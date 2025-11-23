from rodi import Container, Services
from config import settings, Environ
from functools import lru_cache


@lru_cache(1)
def get_container() -> Services:
    if settings.environ is Environ.dev:
        container = LocalContainer().initialize()
    elif settings.environ is Environ.prod:
        container = ProdContainer().initialize()
    return container.build_provider()


class BaseContainer:
    def __inti__(self) -> None:
        self.container = Container()

    def initialize(self) -> Container:
        return self.container


class LocalContainer(BaseContainer):
    def initialize(self) -> Container:
        super().initialize()
        return self.container


class ProdContainer(BaseContainer):
    def initialize(self) -> Container:
        super().initialize()
        return self.container
