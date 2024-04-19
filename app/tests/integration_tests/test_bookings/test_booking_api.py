import pytest
from httpx import AsyncClient


class Test_booking_api:
    @pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
        (4, '2030-04-20', '2030-04-25', 2, 200),
        (4, '2030-04-20', '2030-04-25', 3, 200),
        (4, '2030-04-20', '2030-04-25', 4, 200),
        (4, '2030-04-20', '2030-04-25', 5, 200),
        (4, '2030-04-20', '2030-04-25', 6, 200),
        (4, '2030-04-20', '2030-04-25', 7, 200),
        (4, '2030-04-20', '2030-04-25', 8, 200),
        (4, '2030-04-20', '2030-04-25', 9, 200),
        (4, '2030-04-20', '2030-04-25', 9, 409),
        (4, '2030-04-20', '2030-04-25', 9, 409),

    ])
    async def test_add_booking_api(self, room_id, date_from, date_to, booked_rooms, status_code,
                                   authenticated_ac: AsyncClient):
        response = await authenticated_ac.post(url='/v1/bookings/add', params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        })
        assert response.status_code == status_code

        response = await authenticated_ac.get('/v1/bookings')

        assert len(response.json()) == booked_rooms

    async def test_get_and_delete_booking_api(self, authenticated_ac: AsyncClient):
        response = await authenticated_ac.get('/v1/bookings')
        for booking in response.json():
            await authenticated_ac.delete(url=f'/v1/bookings/{booking['id']}')
        response = await authenticated_ac.get('/v1/bookings')
        assert len(response.json()) == 0
