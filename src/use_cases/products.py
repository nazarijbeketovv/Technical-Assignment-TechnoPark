"""Use case и доменная логика расчёта стоимости изделия."""

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from shared.interfaces.repositories.products import ICalcResultRepository
from shared.interfaces.use_cases.products import (
    CalculateProductCostResultDTO,
    ICalculateProductCostUseCase,
    MaterialDTO,
)


@dataclass(slots=True)
class Material:
    """Доменная модель материала, входящего в изделие."""

    name: str
    qty: Decimal
    price_rub: Decimal


@dataclass(slots=True)
class CalculateProductCostResult:
    """Результат доменного расчёта стоимости изделия."""

    total_cost_rub: Decimal


def calculate_total_cost(
    materials: Iterable[Material],
) -> CalculateProductCostResult:
    """Рассчитать итоговую стоимость изделия по списку материалов.

    Args:
        materials: Коллекция материалов с количеством и ценой.

    Returns:
        Результат расчёта с суммарной стоимостью в рублях.
    """
    total = Decimal("0")
    for material in materials:
        total += material.qty * material.price_rub

    return CalculateProductCostResult(total_cost_rub=total)


class CalculateProductCostUseCase(ICalculateProductCostUseCase):
    """Use case расчёта стоимости изделия и сохранения результата."""

    def __init__(self, repository: ICalcResultRepository) -> None:
        """Создать use case с указанным репозиторием.

        Args:
            repository: Репозиторий для сохранения результата расчёта.
        """
        self._repository = repository

    async def __call__(
        self,
        materials: Iterable[MaterialDTO],
    ) -> CalculateProductCostResultDTO:
        """Рассчитать стоимость изделия и сохранить результат в репозиторий.

        Args:
            materials: Коллекция DTO материалов из внешнего слоя.

        Returns:
            DTO с итоговой стоимостью изделия.
        """
        domain_materials = [
            Material(name=m.name, qty=m.qty, price_rub=m.price_rub)
            for m in materials
        ]

        domain_result = calculate_total_cost(domain_materials)

        await self._repository.save_result(
            total_cost_rub=domain_result.total_cost_rub
        )

        return CalculateProductCostResultDTO(
            total_cost_rub=domain_result.total_cost_rub,
        )
