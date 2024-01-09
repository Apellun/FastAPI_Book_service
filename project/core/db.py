from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
from config import DATABASE_URL

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, future=True)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False,)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

