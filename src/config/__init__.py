"""Настройки приложения и точки входа к конфигурации."""

from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.db import DatabaseSettings


load_dotenv()


__all__ = ("BASE_DIR", "settings")


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Глобальные настройки приложения."""

    debug: bool = Field(default=False, description="Режим отладки")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Минимальный уровень логирования",
    )
    database: DatabaseSettings = Field(
        default_factory=DatabaseSettings,  # type: ignore[arg-type]
    )

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
