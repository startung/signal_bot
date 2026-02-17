from abc import ABC, abstractmethod


class CommandApp(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def handle(self, args: str) -> str: ...
