from signal_bot.app_interface import CommandApp


class TestApp(CommandApp):
    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Reverses the text you send"

    def handle(self, args: str, sender: str = "") -> str:
        return args[::-1]
