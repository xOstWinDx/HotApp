from datetime import datetime

from app.bookings.dao import BookingsDAO


async def test_add_and_get_booking_dao():
    new_booking = await BookingsDAO.add(
        room_id=1,
        date_from=datetime.strptime("2024-04-18", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-04-22", "%Y-%m-%d"),
        user_id=1,
    )
    assert new_booking.room_id == 1
    assert new_booking.user_id == 1

    new_booking = await BookingsDAO.find_by_id(new_booking.id)

    assert new_booking

    await BookingsDAO.delete(new_booking.id, new_booking.user_id)

    new_booking = await BookingsDAO.find_by_id(new_booking.id)

    assert not new_booking
