import json
import subprocess
from datetime import datetime, timezone
from signal_bot.message import Message, Direction


class SignalCli:
    def __init__(self, account: str, cli_path: str = "signal-cli") -> None:
        self.account = account
        self._cli_parts = cli_path.split()

    def _base_cmd(self) -> list[str]:
        return [*self._cli_parts, "-a", self.account]

    def send(self, recipient: str, body: str) -> None:
        cmd = [*self._base_cmd(), "send", "-m", body, recipient]
        subprocess.run(cmd, capture_output=True, text=True, check=True)

    def receive(self) -> list[Message]:
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
                continue
            body = data_message.get("message")
            if body is None:
                continue
            timestamp_ms = envelope.get("timestamp", 0)
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            messages.append(Message(
                sender=envelope.get("source", ""),
                recipient=self.account,
                body=body,
                direction=Direction.INCOMING,
                timestamp=timestamp,
            ))
        return messages
