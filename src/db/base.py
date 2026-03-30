from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.db.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,          # Set True for SQL query logging during dev
    pool_size=10,        # Max persistent connections
    max_overflow=20,     # Extra connections under load
    pool_pre_ping=True,  # Drop stale connections automatically
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass