"""
Класс асинхронных движка и сессии sqlachemy+asyncpg
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager


class Database:

    def __init__(self, db_url: str) -> None:
        self.db_url = db_url 
        self._engine = create_async_engine(self.db_url)
        self._async_session = sessionmaker(bind=self._engine, expire_on_commit=False, class_=AsyncSession)


    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        session = self._async_session()
        yield session
        await session.close()