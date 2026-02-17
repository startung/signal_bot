from signal_bot.app_interface import CommandApp


class AppRegistry:
    def __init__(self) -> None:
        self._apps: dict[str, CommandApp] = {}

    def register(self, app: CommandApp) -> None:
        if app.name in self._apps:
            raise ValueError(f"Command '{app.name}' is already registered")
        self._apps[app.name] = app

    def get(self, command_name: str) -> CommandApp | None:
        return self._apps.get(command_name)
