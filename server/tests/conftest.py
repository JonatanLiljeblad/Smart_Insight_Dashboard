from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.player import Player
from app.models.player_stat import PlayerStat

SQLALCHEMY_TEST_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_player(db_session):
    player = Player(
        external_id="sample-player",
        name="Sample Player",
        nationality="United States",
        tour="PGA Tour",
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)
    return player


@pytest.fixture
def sample_player_stats(db_session, sample_player):
    stats = [
        PlayerStat(
            player_id=sample_player.id,
            event_date=date(2025, 1, 15),
            scoring_average=69.8,
            strokes_gained_total=1.2,
            driving_accuracy=66.4,
            greens_in_regulation=71.5,
            putting_average=1.73,
        ),
        PlayerStat(
            player_id=sample_player.id,
            event_date=date(2025, 2, 5),
            scoring_average=70.1,
            strokes_gained_total=0.9,
            driving_accuracy=64.8,
            greens_in_regulation=69.2,
            putting_average=1.75,
        ),
        PlayerStat(
            player_id=sample_player.id,
            event_date=date(2025, 2, 26),
            scoring_average=69.4,
            strokes_gained_total=1.5,
            driving_accuracy=67.1,
            greens_in_regulation=72.8,
            putting_average=1.71,
        ),
    ]
    db_session.add_all(stats)
    db_session.commit()
    return stats


@pytest.fixture
def auth_token(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "owner@example.com",
            "full_name": "Owner User",
            "password": "secret123",
        },
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "owner@example.com", "password": "secret123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
