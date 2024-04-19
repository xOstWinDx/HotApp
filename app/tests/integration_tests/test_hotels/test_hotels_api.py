import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "date_from,date_to, status_code",
    [
        ("2024-03-15", "2024-03-20", 200),
        ("2024-03-15", "2024-02-20", 400),
        ("2024-03-15", "2024-06-20", 400),
    ],
)
async def test_hotels_api(date_from, date_to, status_code, ac: AsyncClient):
    response = await ac.get(
        url="/v1/hotels/Алтай", params={"date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == status_code
