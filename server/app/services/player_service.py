from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.player import Player
from app.models.player_stat import PlayerStat


class PlayerNotFoundError(Exception):
    pass


def list_players(db: Session, *, skip: int = 0, limit: int = 20) -> list[Player]:
    stmt = select(Player).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_player_or_raise(db: Session, player_id: int) -> Player:
    player = db.get(Player, player_id)
    if not player:
        raise PlayerNotFoundError
    return player


def get_player_stats_or_raise(db: Session, player_id: int) -> list[PlayerStat]:
    get_player_or_raise(db, player_id)
    stmt = (
        select(PlayerStat)
        .where(PlayerStat.player_id == player_id)
        .order_by(PlayerStat.event_date)
    )
    return list(db.scalars(stmt).all())
