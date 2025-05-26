import os
import traceback
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text
from typing import Any

load_dotenv()


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str:, Any]):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(os.getenv("DATABASE_URL"), {"echo": True})


async def get_db():
    async with sessionmanager.session() as session:
        yield session


async def check_db_connected():
    try:
        async with sessionmanager.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database is connected (^_^)")
    except Exception as e:
        print("Looks like there is some problem in connection, see below traceback")
        traceback.print_exc()
        raise e


async def check_db_disconnected():
    try:
        await sessionmanager.close()
        print("Database is Disconnected (-_-) zZZ")
    except Exception as e:
        raise e
