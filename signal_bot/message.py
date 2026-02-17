from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class Direction(Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


@dataclass
class Message:
    sender: str
    recipient: str
    body: str
    direction: Direction
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
