from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.favorite import Favorite
from app.models.player import Player
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteOut

router = APIRouter()


@router.get("/", response_model=list[FavoriteOut])
def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Favorite).where(Favorite.user_id == current_user.id)
    return list(db.scalars(stmt).all())


@router.post("/", response_model=FavoriteOut, status_code=status.HTTP_201_CREATED)
def add_favorite(
    payload: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    player = db.get(Player, payload.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    existing = db.scalars(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.player_id == payload.player_id,
        )
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Already favorited")

    favorite = Favorite(user_id=current_user.id, player_id=payload.player_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    favorite = db.get(Favorite, favorite_id)
    if not favorite or favorite.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
