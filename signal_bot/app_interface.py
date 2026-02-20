from abc import ABC, abstractmethod
from collections.abc import Iterator


class CommandApp(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def handle(self, args: str, sender: str = "") -> Iterator[str]: ...
