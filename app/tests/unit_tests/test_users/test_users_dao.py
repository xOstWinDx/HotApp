import pytest
from httpx import AsyncClient

from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id,email,exsist",
    [
        (1, "fedor@moloko.ru", True),
        (2, "starkatya0@yandex.ru", True),
        (5, "NotExistUser", False),
    ],
)
async def test_user_find_by_id(user_id, email, exsist, ac: AsyncClient):
    user = await UsersDAO.find_by_id(user_id)
    if exsist:
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
