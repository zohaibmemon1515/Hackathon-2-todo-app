from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings

# Neon DB ke liye Sync connection (psycopg2) sabse stable hai
# Ensure settings.database_url starts with 'postgresql://' NOT 'postgresql+asyncpg://'

engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
    pool_recycle=300,
    # Psycopg2 ke liye sslmode use hota hai
    connect_args={"sslmode": "require"} 
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session