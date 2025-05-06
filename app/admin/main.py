import uvicorn
from app.admin.authentication import AdminAuthenticationBackend
from app.admin.views import UserAdmin, ProductAdmin, OrderAdmin
from app.infra.postgres.base import Base
from app.infra.postgres.db import Database
from settings.config import AppSettings
from sqladmin import Admin
from starlette.applications import Starlette


class AdminApplication:
    def __init__(self, app_settings: AppSettings):
        self.web_app = Starlette()
        self.database = Database(app_settings.POSTGRES_DSN, declarative_base=Base)
        self.admin = Admin(self.web_app, self.database.engine,
                           authentication_backend=AdminAuthenticationBackend(settings=app_settings), base_url="/")
        self._register_views()

    def _register_views(self) -> None:
        self.admin.add_view(UserAdmin)
        self.admin.add_view(ProductAdmin)
        self.admin.add_view(OrderAdmin)


def create_app() -> Starlette:
    app = AdminApplication(AppSettings())
    return app.web_app


if __name__ == '__main__':
    settings = AppSettings()
    uvicorn.run(
        "app.admin.main:create_app",
        host="localhost",
        port=settings.ADMIN_INTERFACE_PORT,
        log_level="info",
        workers=1,
    )
