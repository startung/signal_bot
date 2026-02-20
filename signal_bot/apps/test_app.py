from collections.abc import Iterator
from signal_bot.app_interface import CommandApp


class TestApp(CommandApp):
    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Reverses the text you send"

    def handle(self, args: str, sender: str = "") -> Iterator[str]:
        yield args[::-1]
