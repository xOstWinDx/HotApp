from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.exceptions import UserAlreadyExistException
from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_user_admin
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return None


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user: Users = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("my_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("my_access_token")


@router.get("/me")
async def get_user_me(user: Users = Depends(get_current_user)):
    return user


@router.get("/allusers")
async def get_user_all(user: Users = Depends(get_current_user_admin)):
    return await UsersDAO.get_all()
