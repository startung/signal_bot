import logging
from pathlib import Path
from datetime import datetime, timezone
from signal_bot.app_interface import CommandApp
from signal_bot.logging import log_message
from signal_bot.message import Message, Direction
from signal_bot.registry import AppRegistry
from signal_bot.router import route_command
from signal_bot.signal_cli import SignalCli

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, account: str, cli_path: str = "signal-cli", log_dir: Path | str = "logs", allowed_senders: list[str] | None = None, backend=None) -> None:
        self.account = account
        self.signal_cli = backend if backend is not None else SignalCli(account=account, cli_path=cli_path)
        self.registry = AppRegistry()
        self.log_dir = Path(log_dir)
        self.allowed_senders = allowed_senders
        self._modes: dict[str, str] = {}

    def register_app(self, app: CommandApp) -> None:
        self.registry.register(app)

    def _is_authorized(self, sender: str) -> bool:
        if not self.allowed_senders:
            return True
        return sender in self.allowed_senders

    def _handle_mode_command(self, msg: Message) -> str | None:
        from signal_bot.parser import parse_command
        parsed = parse_command(msg.body)
        if parsed is None:
            return None
        if parsed.args == "start" and self.registry.get(parsed.command):
            logger.debug("Mode start: sender=%s entering command=%s", msg.sender, parsed.command)
            self._modes[msg.sender] = parsed.command
            return f"Entered {parsed.command} mode. All messages will be sent to /{parsed.command}. Send /{parsed.command} end to exit."
        if parsed.args == "end" and self._modes.get(msg.sender) == parsed.command:
            logger.debug("Mode end: sender=%s exiting command=%s", msg.sender, parsed.command)
            del self._modes[msg.sender]
            return f"Exited {parsed.command} mode."
        return None

    def _send_response(self, recipient: str, body: str) -> None:
        self.signal_cli.send(recipient, body)
        outgoing = Message(
            sender=self.account,
            recipient=recipient,
            body=body,
            direction=Direction.OUTGOING,
            timestamp=datetime.now(timezone.utc),
        )
        log_message(outgoing, self.log_dir)

    def process_messages(self) -> None:
        messages = self.signal_cli.receive()
        for msg in messages:
            if not self._is_authorized(msg.sender):
                logger.debug("Unauthorized sender %s — dropping message", msg.sender)
                unauthorized_dir = self.log_dir / "unauthorized"
                unauthorized_dir.mkdir(parents=True, exist_ok=True)
                log_message(msg, unauthorized_dir)
                continue
            log_message(msg, self.log_dir)
            mode_response = self._handle_mode_command(msg)
            if mode_response is not None:
                self._send_response(msg.sender, mode_response)
                continue
            response = route_command(msg.body, self.registry, sender=msg.sender)
            if response is None and msg.sender in self._modes:
                app = self.registry.get(self._modes[msg.sender])
                if app is not None:
                    logger.debug("Dispatching to mode app=%s for sender=%s", app.name, msg.sender)
                    response = app.handle(msg.body, sender=msg.sender)
            if response is not None:
                self._send_response(msg.sender, response)
            else:
                logger.debug("No response for message from %s", msg.sender)
