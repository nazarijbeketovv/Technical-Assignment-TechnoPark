"""Утилиты для интеграции DI-контейнера с FastAPI зависимостями."""

from collections.abc import Callable
from collections.abc import Coroutine
from typing import Annotated, Any
from rodi import Services
from fastapi import Depends
from shared.di.container import get_container


def di[T](dep: type[T]) -> Callable[..., Coroutine[Any, Any, T]]:
    """Создать зависимость FastAPI, разрешающую тип из DI-контейнера.

    Args:
        dep: Класс или интерфейс, который необходимо получить из контейнера.

    Returns:
        Функцию-зависимость для использования в `Depends`.
    """

    async def _resolve(
        container: Annotated[Services, Depends(get_container)],
    ) -> T:
        return container.get(dep)

    return _resolve
