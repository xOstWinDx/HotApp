
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user_admin
from app.users.models import Users


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user: Users = await authenticate_user(email, password)

        # Validate username/password credentials
        # And update session
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        user = await get_current_user_admin(request, token=token)
        if user.is_super:
            return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
