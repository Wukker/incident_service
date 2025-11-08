import enum
from pathlib import Path
from tempfile import gettempdir
from typing import List, Union

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """Настройки приложения."""

    # Адрес для запуска приложения
    host: str = "127.0.0.1"
    port: int = 8000
    origins: List[str] = ["*"]
    # Количество воркеров uvicorn
    workers_count: int = 1
    # Включение режима отладки
    reload: bool = False
    # Включение документации
    enable_doc: bool = True

    # Текущее окружение
    environment: str = "prod"

    # Настройки SSL
    ssl_mode: str = "verify-full"

    # Postgres
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "backend"
    db_user: str = "backend"
    db_password: str = "backend"
    DB_POOL_SIZE: int = Field(
        default=30,
        validation_alias="DB_POOL_SIZE",
    )
    DB_MAX_OVERFLOW: int = Field(
        default=10,
        validation_alias="DB_MAX_OVERFLOW",
    )
    DB_ECHO: Union[bool, str] = Field(
        default=False,
        validation_alias="DB_ECHO",
    )

    log_level: LogLevel = LogLevel.INFO

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            path=f"/{self.db_name}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="UCAR_",
        env_file_encoding="utf-8",
        extra="ignore",
        enable_decoding=False,
    )


settings = Settings()
