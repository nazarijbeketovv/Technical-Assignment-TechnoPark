from decimal import Decimal

import pytest

from api.v1.handlers.products import calculate_cost
from api.v1.schemas.products import CalcRequest, MaterialSchema
from shared.interfaces.use_cases.products import (
    CalculateProductCostResultDTO,
    MaterialDTO,
)


class FakeCalculateProductCostUseCase:
    def __init__(self, total_cost: Decimal) -> None:
        self.total_cost = total_cost
        self.received_materials: list[MaterialDTO] = []

    async def __call__(
        self, materials: list[MaterialDTO]
    ) -> CalculateProductCostResultDTO:
        self.received_materials = list(materials)
        return CalculateProductCostResultDTO(total_cost_rub=self.total_cost)


@pytest.mark.asyncio
async def test_calculate_cost_handler_maps_and_returns_response() -> None:
    payload = CalcRequest(
        materials=[
            MaterialSchema(
                name="steel",
                qty=Decimal("2"),
                price_rub=Decimal("10.50"),
            ),
            MaterialSchema(
                name="copper",
                qty=Decimal("1.5"),
                price_rub=Decimal("100"),
            ),
        ]
    )

    expected_total = Decimal("221.00")
    fake_use_case = FakeCalculateProductCostUseCase(total_cost=expected_total)

    response = await calculate_cost(payload=payload, use_case=fake_use_case)

    assert response.total_cost_rub == expected_total

    assert len(fake_use_case.received_materials) == 2

    first, second = fake_use_case.received_materials

    assert first.name == "steel"
    assert first.qty == Decimal("2")
    assert first.price_rub == Decimal("10.50")

    assert second.name == "copper"
    assert second.qty == Decimal("1.5")
    assert second.price_rub == Decimal("100")
