from datetime import date

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.bookings.dao import BookingsDAO
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.logger import logger


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_left(cls, hotel_id: int, date_from: date, date_to: date):
        try:
            room_in_this_hotel = await cls.get_all(hotel_id=hotel_id)
            for room in room_in_this_hotel:
                print(type(date_to - date_from))
                room.__setattr__(
                    "rooms_left",
                    await BookingsDAO.get_left_room_by_id(room.id, date_from, date_to),
                )
                room.__setattr__("total_cost", (date_to - date_from).days * room.price)
            return room_in_this_hotel
        except (SQLAlchemyError, Exception) as e:
            msg = ''
            if isinstance(e, SQLAlchemyError):
                msg = "DataBase Exception"
            elif isinstance(e, Exception):
                msg = "Unknown Exception"
            msg += ":   Cannot get_rooms_left"
            extra = {
                "hotel_id": hotel_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg=msg, extra=extra, exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
