from app.db.session import engine
from app.db.base import Base
import app.models  # noqa: F401 — registers all models


def init_db():
    Base.metadata.create_all(bind=engine)
