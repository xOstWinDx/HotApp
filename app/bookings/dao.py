from datetime import date

from fastapi import HTTPException
from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import get_async_session
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingsDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def get_all(cls, **filter_by):
        try:
            res = None
            async for session in get_async_session():
                query = select(cls.model).filter_by(**filter_by)
                res = await session.execute(query)
                res = res.scalars().all()
                for booking in res:
                    query = select(Rooms).filter_by(id=booking.room_id)
                    res2 = await session.execute(query)
                    room = res2.scalar_one_or_none()
                    booking.__setattr__("image_id", room.image_id)
                    booking.__setattr__("name", room.name)
                    booking.__setattr__("description", room.description)
                    booking.__setattr__("services", room.services)
            return res
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += ":   Cannot get all bookings"
            extra = {}
            for i in filter_by:
                extra[f'input_{i}'] = filter_by[i]
            logger.error(msg=msg, extra=extra)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def get_left_room_by_id(room_id: int, date_from: date, date_to: date):
        try:
            room_left = None
            async for session in get_async_session():
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )
                rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                room_left = await session.execute(rooms_left)
                room_left = room_left.scalar()

            return room_left
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += ":   Cannot find left room"
            extra = {
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg=msg, extra=extra, exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    async def add(cls, room_id: int, date_from: date, date_to: date, user_id):
        try:
            new_book = None
            async for session in get_async_session():
                room_left = await cls.get_left_room_by_id(room_id, date_from, date_to)
                if room_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price = price.scalar()
                    add_boocking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )
                    new_book = await session.execute(add_boocking)
                    await session.commit()
                    new_book = new_book.scalar()
            return new_book
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += ":   Cannot add booking"
            extra = {
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
                "user_id": user_id,
            }
            logger.error(msg=msg, extra=extra, exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    async def delete(cls, id: int, user_id: int):
        try:
            async for session in get_async_session():
                query = delete(Bookings).filter_by(id=id, user_id=user_id)
                await session.execute(query)
                await session.commit()
            return None
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += ":   Cannot delete booking"
            extra = {
                "id": id,
                "user_id": user_id,
            }
            logger.error(msg=msg, extra=extra, exc_info=True)

