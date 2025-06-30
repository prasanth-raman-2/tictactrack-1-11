"""
Database configuration and setup for Tic Tac Toe backend.
Configures SQLAlchemy engine, async session, and metadata base for use across the application.
"""

import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# PUBLIC_INTERFACE
def get_database_url() -> str:
    """Returns the database URL from the environment variable DATABASE_URL."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise EnvironmentError("DATABASE_URL is not set in the environment")
    # Example expected: 'postgresql+asyncpg://user:password@host:port/dbname'
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return db_url


DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


Base = declarative_base()


# PUBLIC_INTERFACE
def get_db_session():
    """Dependency generator for FastAPI routes."""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        session.close()
