"""SQLAlchemy-модели, отражающие таблицы базы данных."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для декларативных моделей SQLAlchemy."""


class CalcResult(Base):
    """Модель результата расчёта стоимости изделия."""

    __tablename__ = "calc_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    total_cost_rub: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        comment="Итоговая стоимость изделия в рублях",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Момент создания записи",
    )


__all__ = ["Base", "CalcResult"]
