from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.services.player_service import get_player_or_raise


class FavoriteConflictError(Exception):
    pass


class FavoriteNotFoundError(Exception):
    pass


def list_favorites(db: Session, *, user_id: int) -> list[Favorite]:
    stmt = select(Favorite).where(Favorite.user_id == user_id)
    return list(db.scalars(stmt).all())


def add_favorite(db: Session, *, user_id: int, player_id: int) -> Favorite:
    get_player_or_raise(db, player_id)

    existing = db.scalars(
        select(Favorite).where(
            Favorite.user_id == user_id,
            Favorite.player_id == player_id,
        )
    ).first()
    if existing:
        raise FavoriteConflictError

    favorite = Favorite(user_id=user_id, player_id=player_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def remove_favorite(db: Session, *, user_id: int, favorite_id: int) -> None:
    favorite = db.get(Favorite, favorite_id)
    if not favorite or favorite.user_id != user_id:
        raise FavoriteNotFoundError

    db.delete(favorite)
    db.commit()
