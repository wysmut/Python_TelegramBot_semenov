from contextlib import asynccontextmanager
from typing import AsyncGenerator

from pydantic import Secret, PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Database:
    def __init__(self, dsn: Secret[PostgresDsn], declarative_base: type[DeclarativeBase]):
        self.engine = create_async_engine(str(dsn.get_secret_value()))
        self._async_session = async_sessionmaker(self.engine)

        self._declarative_base = declarative_base

    async def shutdown(self) -> None:
        await self.engine.dispose()

    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(self._declarative_base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._async_session()

        async with session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
