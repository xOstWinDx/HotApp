import ast
import json
from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.bookings.dao import BookingsDAO
from app.dao.base import BaseDAO
from app.database import get_async_session
from app.hotels.models import Hotels
from app.hotels.rooms.dao import RoomsDAO
from app.logger import logger


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotel_with_rooms_left(cls, location, date_from: date, date_to: date):
        try:
            hotels = None
            async for session in get_async_session():
                query = select(cls.model).filter(
                    cls.model.location.like("%" + location + "%")
                )
                hotels = await session.execute(query)
                hotels = hotels.scalars().all()
                for hotel in hotels:
                    buffer = []
                    for room in await RoomsDAO.get_all(hotel_id=hotel.id):
                        buffer.append(
                            await BookingsDAO.get_left_room_by_id(
                                room["Rooms"].id, date_from, date_to
                            )
                        )
                    hotel.__setattr__("rooms_left", sum(buffer))

                    hotel.services = "\U0001F4CD " + ", ".join(ast.literal_eval(hotel.services))

            return hotels
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += ":   Cannot get_hotel_with_rooms_left"
            extra = {
                "location": location,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg=msg, extra=extra, exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
