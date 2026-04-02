from datetime import date, datetime

from pydantic import BaseModel


class PlayerOut(BaseModel):
    id: int
    external_id: str
    name: str
    nationality: str | None = None
    tour: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PlayerStatOut(BaseModel):
    id: int
    player_id: int
    event_date: date
    scoring_average: float | None = None
    strokes_gained_total: float | None = None
    driving_accuracy: float | None = None
    greens_in_regulation: float | None = None
    putting_average: float | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
