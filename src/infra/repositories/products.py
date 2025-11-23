"""Репозитории для работы с результатами расчёта стоимости изделия."""

from decimal import Decimal
from shared.interfaces.repositories.products import ICalcResultRepository
from infra.database.models import CalcResult
from shared.interfaces.db import IDatabase


class CalcResultRepository(ICalcResultRepository):
    """Репозиторий для сохранения результатов расчёта в таблицу `calc_results`."""

    def __init__(self, db: IDatabase) -> None:
        """Создать экземпляр репозитория.

        Args:
            db: Высокоуровневый сервис доступа к базе данных.
        """
        self._db = db

    async def save_result(self, total_cost_rub: Decimal) -> None:
        """Сохранить итоговую стоимость изделия в базу данных.

        Args:
            total_cost_rub: Рассчитанная итоговая стоимость в рублях.
        """
        async with self._db.get_session() as session:
            obj = CalcResult(total_cost_rub=total_cost_rub)
            session.add(obj)
            await session.flush()
