from fastapi import APIRouter

router = APIRouter()


@router.get("/player/{player_id}/stats")
def get_player_stats(player_id: int):
    # TODO: implement player stats lookup
    return {"player_id": player_id, "stats": {}}
