from collections.abc import Generator
from sqlalchemy.orm import Session

from app.database.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session for each request.
    Yields a SQLAlchemy Session object and ensures it is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()