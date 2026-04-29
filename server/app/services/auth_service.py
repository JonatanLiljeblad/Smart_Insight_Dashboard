from datetime import datetime, timedelta, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.core.security import generate_refresh_token, hash_token
from app.models.auth_session import AuthSession
from app.models.user import User
from app.schemas.auth import RegisterRequest


def _utcnow_naive() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def create_user(db: Session, payload: RegisterRequest) -> User:
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_auth_session(
    db: Session,
    *,
    user_id: int,
    user_agent: str | None = None,
    ip_address: str | None = None,
) -> tuple[AuthSession, str]:
    refresh_token = generate_refresh_token()
    session = AuthSession(
        user_id=user_id,
        refresh_token_hash=hash_token(refresh_token),
        user_agent=user_agent,
        ip_address=ip_address,
        expires_at=_utcnow_naive() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session, refresh_token


def get_auth_session_by_refresh_token(
    db: Session, refresh_token: str
) -> AuthSession | None:
    stmt = select(AuthSession).where(
        AuthSession.refresh_token_hash == hash_token(refresh_token)
    )
    return db.scalars(stmt).first()


def is_auth_session_active(session: AuthSession) -> bool:
    return session.revoked_at is None and session.expires_at > _utcnow_naive()


def rotate_auth_session(db: Session, session: AuthSession) -> str:
    refresh_token = generate_refresh_token()
    session.refresh_token_hash = hash_token(refresh_token)
    session.last_used_at = _utcnow_naive()
    session.expires_at = _utcnow_naive() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    db.commit()
    db.refresh(session)
    return refresh_token


def revoke_auth_session(db: Session, session: AuthSession) -> None:
    session.revoked_at = _utcnow_naive()
    db.commit()
