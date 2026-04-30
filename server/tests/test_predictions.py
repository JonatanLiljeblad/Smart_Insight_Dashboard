from app.models.prediction_job import PredictionJob
from app.models.user import User


def test_create_prediction_job_enqueues_work(
    client,
    auth_headers,
    sample_player,
    monkeypatch,
):
    queued_job_ids: list[int] = []

    def fake_delay(job_id: int) -> None:
        queued_job_ids.append(job_id)

    monkeypatch.setattr("app.api.routes.predictions.run_prediction.delay", fake_delay)

    resp = client.post(
        "/api/predictions/",
        json={"player_id": sample_player.id},
        headers=auth_headers,
    )

    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"
    assert queued_job_ids == [resp.json()["id"]]


def test_create_prediction_requires_existing_player(
    client,
    auth_headers,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.api.routes.predictions.run_prediction.delay",
        lambda job_id: None,
    )

    resp = client.post(
        "/api/predictions/",
        json={"player_id": 999},
        headers=auth_headers,
    )

    assert resp.status_code == 404


def test_get_prediction_status_returns_owned_job(
    client,
    auth_headers,
    sample_player,
    db_session,
):
    owner = db_session.query(User).filter(User.email == "owner@example.com").one()
    job = PredictionJob(player_id=sample_player.id, user_id=owner.id, status="completed")
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    resp = client.get(f"/api/predictions/{job.id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == job.id


def test_get_prediction_status_hides_other_users_jobs(
    client,
    auth_headers,
    sample_player,
    db_session,
):
    other_user = User(
        email="other@example.com",
        full_name="Other User",
        hashed_password="hashed",
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    job = PredictionJob(player_id=sample_player.id, user_id=other_user.id, status="pending")
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    resp = client.get(f"/api/predictions/{job.id}", headers=auth_headers)
    assert resp.status_code == 404
