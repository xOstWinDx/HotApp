from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import CantADDBookingsIncorrectDate
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomsDAO

router = APIRouter(prefix="/hotels", tags=["Отели и Комнаты"])


@router.get("/id/{hotel_id}")
@cache(expire=30)
async def get_hotel_by_id(hotel_id: int):
    return await HotelsDAO.get_all(id=hotel_id)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location(location: str, date_from: date, date_to: date):
    if date_from >= date_to:
        raise CantADDBookingsIncorrectDate
    if (date_to - date_from).days > 30:
        raise CantADDBookingsIncorrectDate
    hotel = await HotelsDAO.get_hotel_with_rooms_left(location, date_from, date_to)
    return hotel


@router.get("/{hotel_id}/rooms")
@cache(expire=30)
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    if date_from >= date_to:
        raise CantADDBookingsIncorrectDate
    if (date_to - date_from).days > 30:
        raise CantADDBookingsIncorrectDate
    rooms = await RoomsDAO.get_rooms_left(hotel_id, date_from, date_to)
    return rooms
