from datetime import date

from fastapi import APIRouter, Depends
from fastapi_versioning import version

from app.bookings.dao import BookingsDAO
from app.bookings.schemas import SBoockings, SBoockingsWithOtherInfo
from app.exceptions import (CantADDBoockingsException,
                            CantADDBookingsIncorrectDate)
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
@version(1)
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[SBoockingsWithOtherInfo]:
    resul = await BookingsDAO.get_all(user_id=user.id)
    return resul


@router.delete("/{id}")
@version(1)
async def delete_booking(id: int, user: Users = Depends(get_current_user)):
    await BookingsDAO.delete(id, user.id)


@router.post("/add")
@version(1)
async def add_bookings(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    if date_from >= date_to:
        raise CantADDBookingsIncorrectDate
    if (date_to - date_from).days > 30:
        raise CantADDBookingsIncorrectDate

    booking = await BookingsDAO.add(room_id, date_from, date_to, user.id)

    if not booking:
        raise CantADDBoockingsException
    booking_dict = SBoockings.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
