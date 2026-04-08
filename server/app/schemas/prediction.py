from datetime import datetime

from pydantic import BaseModel


class PredictionJobCreate(BaseModel):
    player_id: int


class PredictionJobOut(BaseModel):
    id: int
    player_id: int
    status: str
    result: dict | None = None
    error_message: str | None = None
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}
