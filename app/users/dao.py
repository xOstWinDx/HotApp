from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.dao.base import BaseDAO
from app.database import get_async_session
from app.logger import logger
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add(cls, email: str, hashed_password: str):
        try:
            async for session in get_async_session():
                query = insert(cls.model).values(
                    email=email.lower(), hashed_password=hashed_password
                )
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += ":   Cannot get_rooms_left"
            extra = {
                "email": hashed_password,
                "hashed_password": hashed_password
            }
            logger.error(msg=msg, extra=extra, exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
