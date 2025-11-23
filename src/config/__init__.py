from enum import Enum
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.db import DatabaseSettings


load_dotenv()


__all__ = ("settings", "BASE_DIR", "Environ")


BASE_DIR = Path(__file__).parent.parent


class Environ(Enum):
    dev = "dev"
    test = "test"
    prod = "prod"


class Settings(BaseSettings):
    debug: bool = Field(description="Режим отладки")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        description="Минимальный уровень логирования"
    )
    session_idle_timeout: int = Field(
        default=10,
        description="Сколько минут бездействия ожидать до закрытия сессии",
    )
    environ: Environ = Field(
        description="Текущее окружение проекта", default=Environ.dev
    )

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")

    @field_validator("debug", mode="plain")
    def validate_debug_mode(cls, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        elif value == "True":
            return True
        else:
            return False


settings: Settings = Settings()
