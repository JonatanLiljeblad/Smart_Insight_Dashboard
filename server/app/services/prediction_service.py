from sqlalchemy.orm import Session

from app.models.prediction_job import PredictionJob
from app.schemas.prediction import PredictionJobCreate
from app.services.player_service import get_player_or_raise


def create_prediction_job(
    db: Session, payload: PredictionJobCreate, user_id: int
) -> PredictionJob:
    get_player_or_raise(db, payload.player_id)
    job = PredictionJob(
        player_id=payload.player_id,
        user_id=user_id,
        status="pending",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_prediction_job(db: Session, job_id: int) -> PredictionJob | None:
    return db.get(PredictionJob, job_id)
