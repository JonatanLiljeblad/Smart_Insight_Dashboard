from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.player import Player
from app.models.player_stat import PlayerStat
from app.schemas.player import PlayerOut, PlayerStatOut

router = APIRouter()


@router.get("/", response_model=list[PlayerOut])
def list_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(Player).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@router.get("/{player_id}", response_model=PlayerOut)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/{player_id}/stats", response_model=list[PlayerStatOut])
def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    stmt = select(PlayerStat).where(PlayerStat.player_id == player_id).order_by(PlayerStat.event_date)
    return list(db.scalars(stmt).all())
