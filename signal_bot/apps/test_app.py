from signal_bot.app_interface import CommandApp


class TestApp(CommandApp):
    @property
    def name(self) -> str:
        return "test"

    def handle(self, args: str) -> str:
        return args[::-1]
