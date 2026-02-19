import logging
from signal_bot.parser import parse_command
from signal_bot.registry import AppRegistry

logger = logging.getLogger(__name__)


def route_command(body: str, registry: AppRegistry, sender: str = "") -> str | None:
    parsed = parse_command(body)
    if parsed is None:
        return None
    logger.debug("Routing command=%s args=%r from sender=%s", parsed.command, parsed.args, sender)
    app = registry.get(parsed.command)
    if app is None:
        logger.debug("No app registered for command=%s", parsed.command)
        return None
    return app.handle(parsed.args, sender=sender)
