"""Celery task: run ML scoring prediction for a player."""

import logging
from datetime import datetime, UTC

import joblib
import numpy as np
from sqlalchemy import select

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.prediction_job import PredictionJob
from app.models.player_stat import PlayerStat

logger = logging.getLogger(__name__)

MODEL_PATH = "/app/ml_artifacts/scoring_model.joblib"
MIN_STAT_ROWS = 3


@celery_app.task(name="run_prediction")
def run_prediction(job_id: int) -> None:
    db = SessionLocal()
    try:
        job = db.get(PredictionJob, job_id)
        if not job:
            logger.error("PredictionJob %s not found", job_id)
            return

        job.status = "running"
        db.commit()

        model = joblib.load(MODEL_PATH)

        stmt = (
            select(PlayerStat)
            .where(PlayerStat.player_id == job.player_id)
            .order_by(PlayerStat.event_date.desc())
            .limit(5)
        )
        stats = list(db.scalars(stmt).all())

        if len(stats) < MIN_STAT_ROWS:
            job.status = "failed"
            job.error_message = "Not enough stat history for prediction"
            job.completed_at = datetime.now(UTC)
            db.commit()
            return

        recent = stats[:3]
        features = np.array([[
            float(np.mean([float(s.scoring_average) for s in recent if s.scoring_average is not None])),
            float(np.mean([float(s.strokes_gained_total) for s in recent if s.strokes_gained_total is not None])),
            float(np.mean([float(s.driving_accuracy) for s in recent if s.driving_accuracy is not None])),
            float(np.mean([float(s.greens_in_regulation) for s in recent if s.greens_in_regulation is not None])),
            float(np.mean([float(s.putting_average) for s in recent if s.putting_average is not None])),
        ]])

        predicted_score = float(model.predict(features)[0])

        job.status = "completed"
        job.result = {
            "predicted_scoring_average": round(predicted_score, 2),
            "features_used": {
                "avg_scoring_3": round(float(features[0][0]), 2),
                "avg_strokes_gained_3": round(float(features[0][1]), 3),
                "avg_driving_accuracy_3": round(float(features[0][2]), 2),
                "avg_gir_3": round(float(features[0][3]), 2),
                "avg_putting_3": round(float(features[0][4]), 3),
            },
            "model": "RandomForestRegressor",
        }
        job.completed_at = datetime.now(UTC)
        db.commit()

    except Exception as e:
        logger.exception("Prediction job %s failed", job_id)
        db.rollback()
        job = db.get(PredictionJob, job_id)
        if job:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.now(UTC)
            db.commit()
    finally:
        db.close()
