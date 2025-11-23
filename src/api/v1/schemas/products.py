"""Pydantic-схемы запросов и ответов для расчёта стоимости изделия."""

from decimal import Decimal

from pydantic import BaseModel, Field


class MaterialSchema(BaseModel):
    """Описание одного материала, входящего в изделие."""

    name: str = Field(min_length=1)
    qty: Decimal = Field(gt=0, description="Количество материала")
    price_rub: Decimal = Field(
        ge=0,
        description="Цена материала за единицу в рублях",
    )


class CalcRequest(BaseModel):
    """Тело запроса на расчёт стоимости изделия."""

    materials: list[MaterialSchema] = Field(
        min_length=1,
        description="Список материалов изделия",
    )


class CalcResponse(BaseModel):
    """Ответ сервиса с рассчитанной итоговой стоимостью изделия."""

    total_cost_rub: Decimal
