"""Интерфейсы для работы с базой данных на уровне абстракций."""

from abc import abstractmethod
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class IDatabaseConnection(Protocol):
    """Интерфейс низкоуровневого подключения к базе данных."""

    @abstractmethod
    def get_session(self) -> AsyncSession:
        """Вернуть новую асинхронную сессию SQLAlchemy."""
        ...


class IDatabase(Protocol):
    """Интерфейс высокоуровневого сервиса работы с базой данных."""

    @abstractmethod
    @asynccontextmanager
    def get_session(self) -> AsyncIterator[AsyncSession]:
        """Предоставить контекстный менеджер сессии базы данных."""
        ...

    @abstractmethod
    @asynccontextmanager
    def transaction(self) -> AsyncIterator[None]:
        """Предоставить контекстный менеджер явной транзакции."""
        ...
