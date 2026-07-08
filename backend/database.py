from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.config import settings
from typing import AsyncGenerator

# Buat engine async untuk PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Buat factory untuk session database
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False- )

# Dependency untuk menyuntikkan session database ke endpoint API
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session