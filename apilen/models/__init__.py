import asyncio
from typing import AsyncIterator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import models (import หลังสุดเพื่อเลี่ยง circular import)
from .customer_model import *
from .station_model import *
from .vehicle_model import *
from .delivery_staff_model import *
from .parcel_model import *

DATABASE_URL = "postgresql+asyncpg://postgres:p%40ssw0rd@172.17.0.5:5432/apilen"

engine: AsyncEngine = None


async def init_db():
    """Initialize the database engine and create tables."""
    global engine
    engine = create_async_engine(
        DATABASE_URL,
    )
    await create_db_and_tables()


async def create_db_and_tables():
    """Create database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Get async database session."""
    if engine is None:
        raise Exception("Database engine is not initialized. Call init_db() first.")

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


async def close_db():
    """Close database connection."""
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None
