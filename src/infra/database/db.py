"""Реализации абстракций доступа к базе данных на SQLAlchemy async."""

import asyncio
from contextlib import asynccontextmanager
from typing import Any
from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.interfaces.db import IDatabaseConnection


class DatabaseConnection:
    """Подключение к базе данных и фабрика асинхронных сессий."""

    def __init__(self, url: str, extra: dict[str, Any]) -> None:
        """Инициализировать подключение и создать пул сессий.

        Args:
            url: DSN-строка подключения к базе данных.
            extra: Дополнительные параметры для конфигурации пула.
        """
        db_engine = create_async_engine(
            url,
            pool_pre_ping=False,
            isolation_level="READ COMMITTED",
            **extra,
        )
        self._session = async_sessionmaker(
            bind=db_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    def get_session(self) -> AsyncSession:
        """Создать новую асинхронную сессию SQLAlchemy."""
        return self._session()


class Database:
    """Высокоуровневый фасад для работы с сессиями и транзакциями БД."""

    def __init__(self, connection: IDatabaseConnection) -> None:
        """Создать сервис работы с базой данных.

        Args:
            connection: Низкоуровневое подключение, выдающее сессии.
        """
        self.__connection = connection
        self.__in_transaction: bool = False
        self.__transaction_session: AsyncSession | None = None

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """Предоставить сессию для единичной операции вне явной транзакции.

        Если метод вызывается внутри `transaction`, будет использована одна и
        та же сессия до конца транзакции.
        """
        session = await self.__build_session()
        try:
            yield session
        except (SQLAlchemyError, asyncio.CancelledError) as e:
            await session.rollback()
            raise e
        finally:
            if self.__in_transaction:
                await session.flush()
            else:
                await session.commit()
                await session.close()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        """Открыть явную транзакцию с повторным использованием сессии.

        Raises:
            RuntimeError: Если транзакция уже была начата.
        """
        if self.__in_transaction:
            raise RuntimeError("Репозиторий уже начал транзакцию.")

        self.__in_transaction = True
        self.__transaction_session = self.__connection.get_session()
        try:
            yield
        except Exception as e:
            await self.__transaction_session.rollback()
            raise e
        finally:
            await self.__transaction_session.commit()
            await self.__transaction_session.close()
            self.__in_transaction = False
            self.__transaction_session = None

    async def __build_session(self) -> AsyncSession:
        if self.__in_transaction:
            assert self.__transaction_session is not None, (
                "В транзакции не создана сессия"
            )
            return self.__transaction_session
        else:
            return self.__connection.get_session()
