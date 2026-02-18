from signal_bot.parser import parse_command
from signal_bot.registry import AppRegistry


def route_command(body: str, registry: AppRegistry, sender: str = "") -> str | None:
    parsed = parse_command(body)
    if parsed is None:
        return None
    app = registry.get(parsed.command)
    if app is None:
        return None
    return app.handle(parsed.args, sender=sender)
