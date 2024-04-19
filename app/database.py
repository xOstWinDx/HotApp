import json
from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    pass


if settings.MOD == "TEST":
    DATA_BASE_URL = f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    DATABASE_PARAMS = {"poolclass": NullPool, "json_serializer": lambda obj: json.dumps(obj, ensure_ascii=False)}
else:
    DATA_BASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    DATABASE_PARAMS = {"json_serializer": lambda obj: json.dumps(obj,
                                                                 ensure_ascii=False)}  # Это нужно для того что бы при добавление джсона через алхимию русские символы были нормальные
engine = create_async_engine(DATA_BASE_URL, **DATABASE_PARAMS)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker(engine, expire_on_commit=False)() as session:
        print("Сессия открыта")
        yield session
        print("Сессия закрыта")
