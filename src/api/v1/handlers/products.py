"""Обработчики HTTP-запросов для расчёта стоимости изделия."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.v1.schemas.products import CalcRequest, CalcResponse
from shared.di.injector import di
from shared.interfaces.use_cases import ICalculateProductCostUseCase
from shared.interfaces.use_cases.products import MaterialDTO

router = APIRouter(tags=["Calc"])


@router.post(
    "/calc",
    response_model=CalcResponse,
    status_code=status.HTTP_200_OK,
    summary="Рассчитать стоимость изделия",
)
async def calculate_cost(
    payload: CalcRequest,
    use_case: Annotated[
        ICalculateProductCostUseCase,
        Depends(di(ICalculateProductCostUseCase)),
    ],
) -> CalcResponse:
    """Рассчитать стоимость изделия и вернуть итоговую стоимость.

    Args:
        payload: Валидационная схема с перечнем материалов.
        use_case: Приложенный к ручке use case расчёта стоимости изделия.

    Returns:
        Схема ответа с итоговой стоимостью изделия в рублях.
    """
    materials = [
        MaterialDTO(
            name=m.name,
            qty=m.qty,
            price_rub=m.price_rub,
        )
        for m in payload.materials
    ]
    result = await use_case(materials)
    return CalcResponse(total_cost_rub=result.total_cost_rub)
