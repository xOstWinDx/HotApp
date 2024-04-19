import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", 200),
        ("test@test.com", "test", 409),
        ("sasdf", "test", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    request = await ac.post(
        url="/v1/auth/register", json={"email": email, "password": password}
    )
    assert request.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("starkatya0@yandex.ru", "Qw200422", 200),
        ("starkatya0@yandex.ru", "НеВерныйПароль", 401),
        ("Wrong@person.com", "test", 401),
        ("WrongFormat", "test", 422),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    request = await ac.post(
        url="/v1/auth/login", json={"email": email, "password": password}
    )
    assert request.status_code == status_code
