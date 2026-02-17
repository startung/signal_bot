from pathlib import Path
from datetime import datetime, timezone
from signal_bot.app_interface import CommandApp
from signal_bot.logging import log_message
from signal_bot.message import Message, Direction
from signal_bot.registry import AppRegistry
from signal_bot.router import route_command
from signal_bot.signal_cli import SignalCli


class Bot:
    def __init__(self, account: str, cli_path: str = "signal-cli", log_dir: Path | str = "logs") -> None:
        self.account = account
        self.signal_cli = SignalCli(account=account, cli_path=cli_path)
        self.registry = AppRegistry()
        self.log_dir = Path(log_dir)

    def register_app(self, app: CommandApp) -> None:
        self.registry.register(app)

    def process_messages(self) -> None:
        messages = self.signal_cli.receive()
        for msg in messages:
            log_message(msg, self.log_dir)
            response = route_command(msg.body, self.registry)
            if response is not None:
                self.signal_cli.send(msg.sender, response)
                outgoing = Message(
                    sender=self.account,
                    recipient=msg.sender,
                    body=response,
                    direction=Direction.OUTGOING,
                    timestamp=datetime.now(timezone.utc),
                )
                log_message(outgoing, self.log_dir)
