import datetime

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import IncorrectEmailOrPassword
from app.users.dao import UsersDAO
from app.users.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALHORITM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user: Users = await UsersDAO.find_one_or_none(email=email.lower())
    if not user:
        raise IncorrectEmailOrPassword
    if verify_password(password, user.hashed_password):
        return user
    raise IncorrectEmailOrPassword
