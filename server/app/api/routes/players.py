from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.player import PlayerOut, PlayerStatOut
from app.services.player_service import (
    PlayerNotFoundError,
    get_player_or_raise,
    get_player_stats_or_raise,
    list_players as list_players_service,
)

router = APIRouter()


@router.get("/", response_model=list[PlayerOut])
def list_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return list_players_service(db, skip=skip, limit=limit)


@router.get("/{player_id}", response_model=PlayerOut)
def get_player(player_id: int, db: Session = Depends(get_db)):
    try:
        return get_player_or_raise(db, player_id)
    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")


@router.get("/{player_id}/stats", response_model=list[PlayerStatOut])
def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    try:
        return get_player_stats_or_raise(db, player_id)
    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")
