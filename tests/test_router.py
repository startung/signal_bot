from signal_bot.app_interface import CommandApp
from signal_bot.registry import AppRegistry
from signal_bot.router import route_command


class ReverseApp(CommandApp):
    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Reverses text"

    def handle(self, args: str, sender: str = ""):
        yield args[::-1]


def make_registry_with_reverse_app() -> AppRegistry:
    registry = AppRegistry()
    registry.register(ReverseApp())
    return registry


def test_routes_command_to_app():
    registry = make_registry_with_reverse_app()
    result = route_command("/test hello, world!", registry)
    assert list(result) == ["!dlrow ,olleh"]


def test_non_command_returns_none():
    registry = make_registry_with_reverse_app()
    result = route_command("just a regular message", registry)
    assert result is None


def test_unregistered_command_returns_none():
    registry = make_registry_with_reverse_app()
    result = route_command("/unknown do stuff", registry)
    assert result is None


def test_command_with_no_args():
    registry = make_registry_with_reverse_app()
    result = route_command("/test", registry)
    assert list(result) == [""]
