from datetime import datetime

from pydantic import BaseModel


class FavoriteCreate(BaseModel):
    player_id: int


class FavoriteOut(BaseModel):
    id: int
    user_id: int
    player_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
