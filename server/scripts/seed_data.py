"""Seed the database with realistic golf player data."""

import random
from datetime import date, timedelta

from sqlalchemy import select

from app.core.config import settings  # noqa: F401
from app.db.session import SessionLocal
from app.db.base import Base  # noqa: F401
from app.models.player import Player
from app.models.player_stat import PlayerStat
import app.models  # noqa: F401

PLAYERS = [
    ("scottie-scheffler", "Scottie Scheffler", "United States", "PGA Tour"),
    ("rory-mcilroy", "Rory McIlroy", "Northern Ireland", "PGA Tour"),
    ("jon-rahm", "Jon Rahm", "Spain", "LIV Golf"),
    ("viktor-hovland", "Viktor Hovland", "Norway", "PGA Tour"),
    ("xander-schauffele", "Xander Schauffele", "United States", "PGA Tour"),
    ("collin-morikawa", "Collin Morikawa", "United States", "PGA Tour"),
    ("ludvig-aberg", "Ludvig Åberg", "Sweden", "PGA Tour"),
    ("wyndham-clark", "Wyndham Clark", "United States", "PGA Tour"),
    ("matt-fitzpatrick", "Matt Fitzpatrick", "England", "PGA Tour"),
    ("tommy-fleetwood", "Tommy Fleetwood", "England", "DP World Tour"),
    ("hideki-matsuyama", "Hideki Matsuyama", "Japan", "PGA Tour"),
    ("shane-lowry", "Shane Lowry", "Ireland", "PGA Tour"),
    ("cameron-smith", "Cameron Smith", "Australia", "LIV Golf"),
    ("patrick-cantlay", "Patrick Cantlay", "United States", "PGA Tour"),
    ("max-homa", "Max Homa", "United States", "PGA Tour"),
]


def generate_stats(player_id: int, num_events: int = 12) -> list[PlayerStat]:
    """Generate realistic-looking stat rows for a player."""
    random.seed(player_id)
    base_scoring = random.uniform(69.0, 71.5)
    base_sg = random.uniform(0.5, 2.5)
    base_da = random.uniform(58.0, 70.0)
    base_gir = random.uniform(64.0, 74.0)
    base_putting = random.uniform(1.70, 1.82)

    stats = []
    start = date(2025, 1, 15)
    for i in range(num_events):
        event_date = start + timedelta(weeks=i * 3 + random.randint(0, 5))
        stats.append(
            PlayerStat(
                player_id=player_id,
                event_date=event_date,
                scoring_average=round(base_scoring + random.uniform(-1.0, 1.0), 2),
                strokes_gained_total=round(base_sg + random.uniform(-1.5, 1.0), 3),
                driving_accuracy=round(base_da + random.uniform(-5.0, 5.0), 2),
                greens_in_regulation=round(base_gir + random.uniform(-4.0, 4.0), 2),
                putting_average=round(base_putting + random.uniform(-0.06, 0.06), 3),
            )
        )
    return stats


def seed():
    db = SessionLocal()
    try:
        existing = db.scalars(select(Player)).first()
        if existing:
            print("Database already seeded — skipping.")
            return

        players = []
        for ext_id, name, nationality, tour in PLAYERS:
            player = Player(
                external_id=ext_id,
                name=name,
                nationality=nationality,
                tour=tour,
            )
            db.add(player)
            db.flush()
            players.append(player)

            stats = generate_stats(player.id)
            db.add_all(stats)

        db.commit()
        print(f"Seeded {len(players)} players with stats.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
