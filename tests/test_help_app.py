from signal_bot.app_interface import CommandApp
from signal_bot.registry import AppRegistry
from signal_bot.apps.help_app import HelpApp


class FakeApp(CommandApp):
    def __init__(self, cmd_name: str, cmd_description: str):
        self._name = cmd_name
        self._description = cmd_description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def handle(self, args: str, sender: str = ""):
        yield ""


def make_registry_with_help():
    registry = AppRegistry()
    registry.register(FakeApp("test", "Reverses text"))
    registry.register(FakeApp("date", "Shows date/time"))
    help_app = HelpApp(registry)
    registry.register(help_app)
    return registry, help_app


def test_is_a_command_app():
    registry = AppRegistry()
    app = HelpApp(registry)
    assert isinstance(app, CommandApp)


def test_name_is_help():
    registry = AppRegistry()
    app = HelpApp(registry)
    assert app.name == "help"


def test_lists_all_commands():
    registry, help_app = make_registry_with_help()
    response = "\n".join(help_app.handle(""))
    assert "/test" in response
    assert "/date" in response
    assert "/help" in response


def test_includes_descriptions():
    registry, help_app = make_registry_with_help()
    response = "\n".join(help_app.handle(""))
    assert "Reverses text" in response
    assert "Shows date/time" in response


def test_help_has_description():
    registry = AppRegistry()
    app = HelpApp(registry)
    assert app.description
