from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# create a connection engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)