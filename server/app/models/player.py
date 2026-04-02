from datetime import datetime, UTC

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    nationality: Mapped[str | None] = mapped_column(String(100), default=None)
    tour: Mapped[str | None] = mapped_column(String(50), default=None)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    stats: Mapped[list["PlayerStat"]] = relationship(back_populates="player")  # noqa: F821
    favorited_by: Mapped[list["Favorite"]] = relationship(back_populates="player")  # noqa: F821
