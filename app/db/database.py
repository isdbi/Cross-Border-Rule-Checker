# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.config.config import Settings

settings = Settings()

# Sync engine (for migrations)
engine = create_engine(settings.database_url)

# Async engine (for Neon)
async_engine = create_async_engine(settings.async_database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession  # For async support
)

async def get_db():
    async with SessionLocal() as session:
        yield session