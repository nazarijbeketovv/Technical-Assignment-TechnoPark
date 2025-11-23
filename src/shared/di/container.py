"""Определение DI-контейнера и регистрация зависимостей приложения."""

from functools import lru_cache

from rodi import Container, Services

from config import settings
from infra.database.db import Database, DatabaseConnection
from infra.repositories.products import CalcResultRepository
from shared.interfaces.db import IDatabase, IDatabaseConnection
from shared.interfaces.repositories.products import ICalcResultRepository
from shared.interfaces.use_cases import ICalculateProductCostUseCase
from use_cases.products import CalculateProductCostUseCase


@lru_cache(1)
def get_container() -> Services:
    """Создать и закэшировать провайдер контейнера зависимостей."""
    container = DiContainer().initialize()

    return container.build_provider()


class DiContainer:
    """DI-контейнер приложения и его конфигурация."""

    def __init__(self) -> None:
        """Инициализировать пустой контейнер Rodi."""
        self.container = Container()

    def _configure_database(self) -> None:
        def db_connection_factory() -> IDatabaseConnection:
            return DatabaseConnection(
                url=settings.database.url,
                extra=settings.database.pool_conf,
            )

        self.container.add_singleton_by_factory(
            db_connection_factory,
            IDatabaseConnection,
        )
        self.container.add_scoped(IDatabase, Database)

    def _configure_repositories(self) -> None:
        self.container.register(ICalcResultRepository, CalcResultRepository)

    def _configure_use_cases(self) -> None:
        self.container.register(
            ICalculateProductCostUseCase,
            CalculateProductCostUseCase,
        )

    def initialize(self) -> Container:
        """Зарегистрировать все зависимости и вернуть настроенный контейнер."""
        self._configure_database()
        self._configure_repositories()
        self._configure_use_cases()
        return self.container
