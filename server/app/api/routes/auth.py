from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.user import UserOut
from app.services.auth_service import (
    authenticate_user,
    create_auth_session,
    create_user,
    get_auth_session_by_refresh_token,
    get_user_by_email,
    is_auth_session_active,
    revoke_auth_session,
    rotate_auth_session,
)

router = APIRouter()


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/auth",
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        path="/api/auth",
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, payload)
    return user


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    _, refresh_token = create_auth_session(
        db,
        user_id=user.id,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    _set_refresh_cookie(response, refresh_token)
    return Token(access_token=create_access_token(subject=user.id))


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    response: Response,
    refresh_token: str | None = Cookie(
        default=None, alias=settings.REFRESH_TOKEN_COOKIE_NAME
    ),
    db: Session = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh session not found")

    session = get_auth_session_by_refresh_token(db, refresh_token)
    if not session or not is_auth_session_active(session):
        if session and session.revoked_at is None:
            revoke_auth_session(db, session)
        raise HTTPException(status_code=401, detail="Refresh session is invalid")

    new_refresh_token = rotate_auth_session(db, session)
    _set_refresh_cookie(response, new_refresh_token)
    return Token(access_token=create_access_token(subject=session.user_id))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    refresh_token: str | None = Cookie(
        default=None, alias=settings.REFRESH_TOKEN_COOKIE_NAME
    ),
    db: Session = Depends(get_db),
):
    if refresh_token:
        session = get_auth_session_by_refresh_token(db, refresh_token)
        if session and is_auth_session_active(session):
            revoke_auth_session(db, session)

    _clear_refresh_cookie(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return None


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
