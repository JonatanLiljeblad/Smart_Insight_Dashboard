from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.prediction import PredictionJobCreate, PredictionJobOut
from app.services.prediction_service import create_prediction_job, get_prediction_job
from app.tasks.prediction_tasks import run_prediction

router = APIRouter()


@router.post("/", response_model=PredictionJobOut, status_code=201)
def request_prediction(
    payload: PredictionJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = create_prediction_job(db, payload, current_user.id)
    run_prediction.delay(job.id)
    return job


@router.get("/{job_id}", response_model=PredictionJobOut)
def get_prediction_status(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_prediction_job(db, job_id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Prediction job not found")
    return job
