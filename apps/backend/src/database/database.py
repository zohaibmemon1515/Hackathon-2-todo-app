from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings

# Create the database engine (Neon Serverless compatible)
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"}
)



def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session
    """
    with Session(engine) as session:
        yield session
