import datetime

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from starlette import status
from starlette.requests import Request

from app.config import settings
from app.exceptions import (TokenNoHasUserIDException,
                            TokenWasExpiredException,
                            UncorrectableTokenException, UserNotFoundException,
                            UserNotIsSuperException)
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    access_token = request.cookies.get("my_access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return access_token


def get_current_user(isSuperUser: bool = False):
    async def getuser(request: Request, token: str = Depends(get_token)):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALHORITM)
        except JWTError:
            request.session.clear()
            raise UncorrectableTokenException

        expire = payload.get("exp")
        if (not expire) or (
            int(expire) < datetime.datetime.now(datetime.UTC).timestamp()
        ):
            raise TokenWasExpiredException

        user_id = payload.get("sub")
        if not user_id:
            raise TokenNoHasUserIDException

        user: Users = await UsersDAO.find_by_id(int(user_id))
        if not user:
            raise UserNotFoundException

        if isSuperUser:

            if not user.is_super:
                raise UserNotIsSuperException

        return user

    return getuser


get_current_user_admin = get_current_user(isSuperUser=True)
get_current_user = get_current_user()
