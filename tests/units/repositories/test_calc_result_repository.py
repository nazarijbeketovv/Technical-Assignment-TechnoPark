from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from decimal import Decimal

import pytest

from infra.database.models import CalcResult
from infra.repositories.products import CalcResultRepository


class FakeAsyncSession:
    def __init__(self) -> None:
        self.added: list[object] = []
        self.flushed: bool = False

    def add(self, obj: object) -> None:
        self.added.append(obj)

    async def flush(self) -> None:
        self.flushed = True


class FakeDatabase:
    def __init__(self, session: FakeAsyncSession) -> None:
        self._session = session

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[FakeAsyncSession]:
        yield self._session


@pytest.mark.asyncio
async def test_calc_result_repository_saves_result() -> None:
    session = FakeAsyncSession()
    db = FakeDatabase(session)
    repo = CalcResultRepository(db)

    total = Decimal("123.45")

    await repo.save_result(total_cost_rub=total)

    assert len(session.added) == 1
    obj = session.added[0]

    assert isinstance(obj, CalcResult)
    assert obj.total_cost_rub == total
    assert session.flushed is True
