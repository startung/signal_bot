import json
import logging
import socket
from datetime import datetime, timezone
from signal_bot.message import Message, Direction

logger = logging.getLogger(__name__)

_request_id = 0


def _next_id() -> int:
    global _request_id
    _request_id += 1
    return _request_id


class SignalCliJsonRpc:
    def __init__(self, account: str, host: str = "localhost", port: int = 7583) -> None:
        self.account = account
        self.host = host
        self.port = port

    def _call(self, method: str, params: dict) -> object:
        request = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": _next_id(),
        }) + "\n"
        logger.debug("JSON-RPC %s -> %s:%s", method, self.host, self.port)
        with socket.create_connection((self.host, self.port)) as sock:
            sock.sendall(request.encode())
            buf = b""
            while b"\n" not in buf:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                buf += chunk
        response = json.loads(buf.split(b"\n")[0])
        if "error" in response:
            raise RuntimeError(f"JSON-RPC error: {response['error']}")
        return response.get("result")

    def send(self, recipient: str, body: str) -> None:
        logger.debug("Sending message to %s", recipient)
        self._call("send", {
            "account": self.account,
            "recipient": [recipient],
            "message": body,
        })

    def receive(self) -> list[Message]:
        logger.debug("Polling for messages via JSON-RPC")
        result = self._call("receive", {"account": self.account})
        messages = []
        for item in result or []:
            envelope = item.get("envelope", {})
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
