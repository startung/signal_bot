import pytest
from signal_bot.app_interface import CommandApp
from signal_bot.registry import AppRegistry


class FakeAppA(CommandApp):
    @property
    def name(self) -> str:
        return "alpha"

    @property
    def description(self) -> str:
        return "App A"

    def handle(self, args: str, sender: str = "") -> str:
        return "a"


class FakeAppB(CommandApp):
    @property
    def name(self) -> str:
        return "beta"

    @property
    def description(self) -> str:
        return "App B"

    def handle(self, args: str, sender: str = "") -> str:
        return "b"


class DuplicateApp(CommandApp):
    @property
    def name(self) -> str:
        return "alpha"

    @property
    def description(self) -> str:
        return "Duplicate"

    def handle(self, args: str, sender: str = "") -> str:
        return "duplicate"


def test_register_and_lookup():
    registry = AppRegistry()
    app = FakeAppA()
    registry.register(app)
    assert registry.get("alpha") is app


def test_register_multiple_apps():
    registry = AppRegistry()
    app_a = FakeAppA()
    app_b = FakeAppB()
    registry.register(app_a)
    registry.register(app_b)
    assert registry.get("alpha") is app_a
    assert registry.get("beta") is app_b


def test_lookup_unregistered_returns_none():
    registry = AppRegistry()
    assert registry.get("nonexistent") is None


def test_duplicate_registration_raises_error():
    registry = AppRegistry()
    registry.register(FakeAppA())
    with pytest.raises(ValueError):
        registry.register(DuplicateApp())
