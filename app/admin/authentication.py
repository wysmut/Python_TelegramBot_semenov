import uuid

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from settings.config import AppSettings


class AdminAuthenticationBackend(AuthenticationBackend):
    def __init__(self, settings: AppSettings):
        super().__init__(secret_key=settings.ADMIN_SECRET_KEY.get_secret_value())

        self.admin_login = settings.ADMIN_LOGIN
        self.admin_password = settings.ADMIN_PASSWORD

        self._admin_session_token: str | None = None

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == self.admin_login.get_secret_value() and password == self.admin_password.get_secret_value():
            self._admin_session_token = str(uuid.uuid4())
            request.session.update({"token": self._admin_session_token})
            return True
        return False

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token or token != self._admin_session_token:
            return False

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
