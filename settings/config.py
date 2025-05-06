import os

from pydantic import SecretStr, PostgresDsn, Secret
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), ".envs/.env"))

    TELEGRAM_API_KEY: SecretStr = SecretStr("secret")
    LOG_LEVEL: str = "INFO"

    POSTGRES_DSN: Secret[PostgresDsn] = Secret(
        PostgresDsn("postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"))

    ADMIN_INTERFACE_PORT: int = 8001
    ADMIN_SECRET_KEY: SecretStr = SecretStr("secretkey")
    ADMIN_LOGIN: SecretStr = SecretStr("admin")
    ADMIN_PASSWORD: SecretStr = SecretStr("admin")

    PERSISTANCE_POSTGRES_DSN: Secret[PostgresDsn] = Secret(
        PostgresDsn("postgresql://postgres:postgres@localhost:5432/postgres"))
