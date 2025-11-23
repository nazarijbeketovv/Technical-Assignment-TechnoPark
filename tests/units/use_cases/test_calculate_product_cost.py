from decimal import Decimal

import pytest

from shared.interfaces.use_cases.products import MaterialDTO
from use_cases.products import (
    CalculateProductCostResult,
    CalculateProductCostUseCase,
    Material,
    calculate_total_cost,
)


class FakeCalcResultRepository:
    def __init__(self) -> None:
        self.saved_total_cost: Decimal | None = None

    async def save_result(self, total_cost_rub: Decimal) -> None:
        self.saved_total_cost = total_cost_rub


def test_calculate_total_cost_single_material() -> None:
    materials = [
        Material(
            name="steel",
            qty=Decimal("2"),
            price_rub=Decimal("10.50"),
        ),
    ]

    result: CalculateProductCostResult = calculate_total_cost(materials)

    assert result.total_cost_rub == Decimal("21.00")


def test_calculate_total_cost_multiple_materials() -> None:
    materials = [
        Material(name="steel", qty=Decimal("2"), price_rub=Decimal("10.50")),
        Material(name="copper", qty=Decimal("1.5"), price_rub=Decimal("100")),
    ]

    result = calculate_total_cost(materials)

    expected = Decimal("2") * Decimal("10.50") + Decimal("1.5") * Decimal("100")
    assert result.total_cost_rub == expected


def test_calculate_total_cost_empty_list() -> None:
    result = calculate_total_cost([])

    assert result.total_cost_rub == Decimal("0")


@pytest.mark.asyncio
async def test_use_case_calls_repository_and_returns_dto() -> None:
    repo = FakeCalcResultRepository()
    use_case = CalculateProductCostUseCase(repository=repo)

    materials_dto = [
        MaterialDTO(name="steel", qty=Decimal("2"), price_rub=Decimal("10.50")),
        MaterialDTO(name="copper", qty=Decimal("1.5"), price_rub=Decimal("100")),
    ]

    result_dto = await use_case(materials_dto)

    expected = Decimal("2") * Decimal("10.50") + Decimal("1.5") * Decimal("100")

    assert result_dto.total_cost_rub == expected
    assert repo.saved_total_cost == expected
