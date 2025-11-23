"""DTO и интерфейс use case расчёта стоимости изделия."""

from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from collections.abc import Iterable


@dataclass(slots=True)
class CalculateProductCostResultDTO:
    """DTO результата расчёта стоимости изделия."""

    total_cost_rub: Decimal


@dataclass(slots=True)
class MaterialDTO:
    """DTO описания материала, участвующего в расчёте изделия."""

    name: str
    qty: Decimal
    price_rub: Decimal


class ICalculateProductCostUseCase(Protocol):
    """Контракт сценария использования расчёта стоимости изделия."""

    @abstractmethod
    async def __call__(
        self,
        materials: Iterable[MaterialDTO],
    ) -> CalculateProductCostResultDTO:
        """Выполнить расчёт стоимости изделия по переданным материалам."""
        ...
