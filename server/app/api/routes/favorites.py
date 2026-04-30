from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteOut
from app.services.favorite_service import (
    FavoriteConflictError,
    FavoriteNotFoundError,
    add_favorite as add_favorite_service,
    list_favorites as list_favorites_service,
    remove_favorite as remove_favorite_service,
)
from app.services.player_service import PlayerNotFoundError

router = APIRouter()


@router.get("/", response_model=list[FavoriteOut])
def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_favorites_service(db, user_id=current_user.id)


@router.post("/", response_model=FavoriteOut, status_code=status.HTTP_201_CREATED)
def add_favorite(
    payload: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return add_favorite_service(
            db,
            user_id=current_user.id,
            player_id=payload.player_id,
        )
    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")
    except FavoriteConflictError:
        raise HTTPException(status_code=409, detail="Already favorited")


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        remove_favorite_service(db, user_id=current_user.id, favorite_id=favorite_id)
    except FavoriteNotFoundError:
        raise HTTPException(status_code=404, detail="Favorite not found")
