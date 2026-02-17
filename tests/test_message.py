from datetime import datetime, timezone
from signal_bot.message import Message, Direction


def test_create_message_incoming():
    msg = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="Hello, bot!",
        direction=Direction.INCOMING,
    )
    assert msg.sender == "+1234567890"
    assert msg.recipient == "+0987654321"
    assert msg.body == "Hello, bot!"
    assert msg.direction == Direction.INCOMING


def test_create_message_outgoing():
    msg = Message(
        sender="+0987654321",
        recipient="+1234567890",
        body="Hi there!",
        direction=Direction.OUTGOING,
    )
    assert msg.direction == Direction.OUTGOING


def test_message_timestamp_defaults_to_now():
    before = datetime.now(timezone.utc)
    msg = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="Test",
        direction=Direction.INCOMING,
    )
    after = datetime.now(timezone.utc)
    assert before <= msg.timestamp <= after


def test_message_timestamp_can_be_set():
    ts = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    msg = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="Test",
        direction=Direction.INCOMING,
        timestamp=ts,
    )
    assert msg.timestamp == ts


def test_direction_values():
    assert Direction.INCOMING.value == "incoming"
    assert Direction.OUTGOING.value == "outgoing"
