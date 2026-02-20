from collections.abc import Iterator
from signal_bot.app_interface import CommandApp
from signal_bot.registry import AppRegistry


class HelpApp(CommandApp):
    def __init__(self, registry: AppRegistry) -> None:
        self._registry = registry

    @property
    def name(self) -> str:
        return "help"

    @property
    def description(self) -> str:
        return "Lists all available commands"

    def handle(self, args: str, sender: str = "") -> Iterator[str]:
        lines = ["Available commands:", ""]
        for app in self._registry.all_apps():
            lines.append(f"/{app.name} — {app.description}")
        yield "\n".join(lines)
