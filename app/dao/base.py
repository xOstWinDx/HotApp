from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.database import get_async_session
from app.logger import logger


class BaseDAO:
    model: object = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            res = None
            async for session in get_async_session():
                query = select(cls.model).filter_by(id=model_id)
                res = await session.execute(query)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += f":   Cannot find by id {cls.model.__name__}"
            extra = {"input_model_id": model_id}
            logger.error(msg=msg, extra=extra, exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            res = None
            async for session in get_async_session():
                query = select(cls.model).filter_by(**filter_by)
                res = await session.execute(query)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += f":   Cannot find one or none {cls.model.__name__}"
            extra = {}
            for i in filter_by:
                extra[f'input_{i}'] = filter_by[i]
            logger.error(msg=msg, extra=extra,exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    async def get_all(cls, **filter_by):
        try:
            res = None
            async for session in get_async_session():
                query = select(cls.model).filter_by(**filter_by)
                res = await session.execute(query)
            return res.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += f":   Cannot get all {cls.model.__name__}"
            extra = {}
            for i in filter_by:
                extra[f'input_{i}'] = filter_by[i]
            logger.error(msg=msg, extra=extra,exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    async def add(cls, **data):
        try:
            async for session in get_async_session():
                query = insert(cls.model).values(**data)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            msg = ""
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += f":   Cannot add {cls.model.__name__}"

            extra = {}
            for i in data:
                extra[f'input_{i}'] = data[i]
            logger.error(msg=msg, extra=extra,exc_info=False)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
