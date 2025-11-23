from abc import abstractmethod
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class IDatabaseConnection(Protocol):
    @abstractmethod
    def get_session(self) -> AsyncSession: ...


class IDatabase(Protocol):
    @abstractmethod
    @asynccontextmanager
    def get_session(self) -> AsyncIterator[AsyncSession]: ...

    @abstractmethod
    @asynccontextmanager
    def transaction(self) -> AsyncIterator[None]: ...
