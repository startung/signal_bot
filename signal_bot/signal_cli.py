import json
import logging
import subprocess
from datetime import datetime, timezone
from signal_bot.message import Message, Direction

logger = logging.getLogger(__name__)


class SignalCli:
    def __init__(self, account: str, cli_path: str = "signal-cli") -> None:
        self.account = account
        self._cli_parts = cli_path.split()

    def _base_cmd(self) -> list[str]:
        return [*self._cli_parts, "-a", self.account]

    def send(self, recipient: str, body: str) -> None:
        logger.debug("Sending message to %s", recipient)
        cmd = [*self._base_cmd(), "send", "-m", body, recipient]
        subprocess.run(cmd, capture_output=True, text=True, check=True)

    def receive(self) -> list[Message]:
        logger.debug("Polling for messages")
        cmd = [*self._base_cmd(), "--output=json", "receive"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        messages = []
        for line in result.stdout.strip().splitlines():
            if not line:
                continue
            data = json.loads(line)
            envelope = data.get("envelope", {})
            data_message = envelope.get("dataMessage")
            if data_message is None:
                logger.debug("Skipping envelope with no dataMessage (source=%s)", envelope.get("source", "unknown"))
                continue
            body = data_message.get("message")
            if body is None:
                logger.debug("Skipping dataMessage with no message body (source=%s)", envelope.get("source", "unknown"))
                continue
            timestamp_ms = envelope.get("timestamp", 0)
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            sender = envelope.get("source", "")
            logger.debug("Parsed incoming message from %s", sender)
            messages.append(Message(
                sender=sender,
                recipient=self.account,
                body=body,
                direction=Direction.INCOMING,
                timestamp=timestamp,
            ))
        return messages
