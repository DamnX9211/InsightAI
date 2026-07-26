from app.database.base import Base
from app.database.session import engine

# Import all models so SQLAlchemy knows about them
from app.models import Dataset


def init_db() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)