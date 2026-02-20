import pytest
from signal_bot.app_interface import CommandApp


class ReverseApp(CommandApp):
    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Reverses text"

    def handle(self, args: str, sender: str = ""):
        yield args[::-1]


class IncompleteApp(CommandApp):
    pass


def test_concrete_app_can_be_instantiated():
    app = ReverseApp()
    assert app is not None


def test_app_has_name():
    app = ReverseApp()
    assert app.name == "test"


def test_app_handle_returns_response():
    app = ReverseApp()
    assert list(app.handle("hello, world!")) == ["!dlrow ,olleh"]


def test_app_handle_empty_args():
    app = ReverseApp()
    assert list(app.handle("")) == [""]


def test_incomplete_app_cannot_be_instantiated():
    with pytest.raises(TypeError):
        IncompleteApp()
