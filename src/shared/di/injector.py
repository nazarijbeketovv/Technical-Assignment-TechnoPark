from collections.abc import Callable
from collections.abc import Coroutine
from typing import Annotated, Any
from rodi import Services
from fastapi import Depends
from shared.di.container import get_container


def di[T](dep: type[T]) -> Callable[..., Coroutine[Any, Any, T]]:
    async def _resolve(
        container: Annotated[Services, Depends(get_container)],
    ) -> T:
        return container.get(dep)

    return _resolve
