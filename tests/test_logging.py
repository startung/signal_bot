import os
from datetime import datetime, timezone
from signal_bot.message import Message, Direction
from signal_bot.logging import log_message


def test_log_creates_file_with_date_name(tmp_path):
    msg = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="Hello!",
        direction=Direction.INCOMING,
        timestamp=datetime(2025, 3, 15, 10, 30, 0, tzinfo=timezone.utc),
    )
    log_message(msg, log_dir=tmp_path)
    expected_file = tmp_path / "2025_03_15.txt"
    assert expected_file.exists()


def test_log_entry_contains_message_details(tmp_path):
    ts = datetime(2025, 3, 15, 10, 30, 0, tzinfo=timezone.utc)
    msg = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="Hello!",
        direction=Direction.INCOMING,
        timestamp=ts,
    )
    log_message(msg, log_dir=tmp_path)
    content = (tmp_path / "2025_03_15.txt").read_text()
    assert "2025-03-15T10:30:00" in content
    assert "incoming" in content
    assert "+1234567890" in content
    assert "+0987654321" in content
    assert "Hello!" in content


def test_multiple_messages_same_day_append(tmp_path):
    msg1 = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="First",
        direction=Direction.INCOMING,
        timestamp=datetime(2025, 3, 15, 10, 0, 0, tzinfo=timezone.utc),
    )
    msg2 = Message(
        sender="+0987654321",
        recipient="+1234567890",
        body="Second",
        direction=Direction.OUTGOING,
        timestamp=datetime(2025, 3, 15, 14, 0, 0, tzinfo=timezone.utc),
    )
    log_message(msg1, log_dir=tmp_path)
    log_message(msg2, log_dir=tmp_path)
    content = (tmp_path / "2025_03_15.txt").read_text()
    lines = content.strip().split("\n")
    assert len(lines) == 2
    assert "First" in lines[0]
    assert "Second" in lines[1]


def test_different_day_creates_new_file(tmp_path):
    msg1 = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="Day one",
        direction=Direction.INCOMING,
        timestamp=datetime(2025, 3, 15, 23, 59, 0, tzinfo=timezone.utc),
    )
    msg2 = Message(
        sender="+1234567890",
        recipient="+0987654321",
        body="Day two",
        direction=Direction.INCOMING,
        timestamp=datetime(2025, 3, 16, 0, 1, 0, tzinfo=timezone.utc),
    )
    log_message(msg1, log_dir=tmp_path)
    log_message(msg2, log_dir=tmp_path)
    assert (tmp_path / "2025_03_15.txt").exists()
    assert (tmp_path / "2025_03_16.txt").exists()
    assert "Day one" in (tmp_path / "2025_03_15.txt").read_text()
    assert "Day two" in (tmp_path / "2025_03_16.txt").read_text()
