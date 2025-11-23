"""Конфигурация подключения к базе данных Postgres."""

from urllib.parse import quote

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Настройки подключения и пула соединений к Postgres."""

    host: str = Field(description="Хост размещения БД")
    port: int = Field(description="Порт подключения к Postgres", ge=0, le=65535)
    database: str = Field(description="Название БД Postgres")
    user: str = Field(description="Имя пользователя Postgres")
    password: str = Field(description="Пароль пользователя Postgres")
    pool_size: int = Field(
        default=10, description="Количество постоянных соединений в пуле"
    )
    max_overflow: int = Field(
        default=20, description="Сколько можно открыть сверх pool_size"
    )
    pool_timeout: int = Field(
        default=30,
        description="Сколько секунд ждать свободного соединения из пула",
    )
    pool_recycle: int = Field(
        default=3600, description="Время жизни соединений в пуле"
    )

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_", case_sensitive=False, extra="ignore"
    )

    @property
    def url(self) -> str:
        """Сформировать DSN-строку подключения к Postgres."""
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=quote(self.password),
                host=self.host,
                port=self.port,
                path=self.database,
            )
        )

    @property
    def pool_conf(self) -> dict[str, int]:
        """Вернуть параметры пула соединений для SQLAlchemy-движка."""
        return {
            "max_overflow": self.max_overflow,
            "pool_timeout": self.pool_timeout,
            "pool_recycle": self.pool_recycle,
            "pool_size": self.pool_size,
        }
