from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings
import os

# Neon DB ke liye Sync connection (psycopg2) sabse stable hai
# Ensure settings.database_url starts with 'postgresql://' NOT 'postgresql+asyncpg://'

# For AI Chatbot feature, we can use the same database configuration
DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    echo=settings.db_echo,
    pool_pre_ping=True,
    pool_recycle=300,
    # Psycopg2 ke liye sslmode use hota hai
    connect_args={"sslmode": "require"}
)

def get_engine():
    """Return the database engine instance."""
    return engine

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session