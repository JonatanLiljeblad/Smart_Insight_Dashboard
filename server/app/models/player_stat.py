from datetime import date, datetime, UTC

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PlayerStat(Base):
    __tablename__ = "player_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    event_date: Mapped[date]
    scoring_average: Mapped[float | None] = mapped_column(Numeric(5, 2), default=None)
    strokes_gained_total: Mapped[float | None] = mapped_column(Numeric(6, 3), default=None)
    driving_accuracy: Mapped[float | None] = mapped_column(Numeric(5, 2), default=None)
    greens_in_regulation: Mapped[float | None] = mapped_column(Numeric(5, 2), default=None)
    putting_average: Mapped[float | None] = mapped_column(Numeric(5, 3), default=None)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    player: Mapped["Player"] = relationship(back_populates="stats")  # noqa: F821
