"""Интерфейс репозитория для сохранения результатов расчёта изделия."""

from typing import Protocol
from abc import abstractmethod
from decimal import Decimal


class ICalcResultRepository(Protocol):
    """Контракт репозитория для работы с результатами расчёта."""

    @abstractmethod
    async def save_result(self, total_cost_rub: Decimal) -> None:
        """Сохранить итоговую стоимость изделия."""
        ...
