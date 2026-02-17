from signal_bot.app_interface import CommandApp
from signal_bot.apps.test_app import TestApp


def test_is_a_command_app():
    app = TestApp()
    assert isinstance(app, CommandApp)


def test_name_is_test():
    app = TestApp()
    assert app.name == "test"


def test_reverses_text():
    app = TestApp()
    assert app.handle("hello, world!") == "!dlrow ,olleh"


def test_empty_args_returns_empty():
    app = TestApp()
    assert app.handle("") == ""


def test_reverses_single_word():
    app = TestApp()
    assert app.handle("abc") == "cba"
