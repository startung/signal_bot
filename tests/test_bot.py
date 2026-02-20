from datetime import datetime, timezone
from unittest.mock import patch, MagicMock, call
from signal_bot.bot import Bot
from signal_bot.app_interface import CommandApp
from signal_bot.message import Message, Direction


class ReverseApp(CommandApp):
    @property
    def name(self) -> str:
        return "test"

    @property
    def description(self) -> str:
        return "Reverses text"

    def handle(self, args: str, sender: str = ""):
        yield args[::-1]


def make_message(body, sender="+440001111111"):
    return Message(
        sender=sender,
        recipient="+447786000000",
        body=body,
        direction=Direction.INCOMING,
        timestamp=datetime(2025, 3, 15, 10, 0, 0, tzinfo=timezone.utc),
    )


def make_bot(tmp_path):
    bot = Bot(account="+447786000000", cli_path="signal-cli", log_dir=tmp_path)
    bot.register_app(ReverseApp())
    return bot


def test_command_message_sends_response(tmp_path):
    bot = make_bot(tmp_path)
    msg = make_message("/test hello, world!")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_called_once_with("+440001111111", "!dlrow ,olleh")


def test_non_command_message_no_response(tmp_path):
    bot = make_bot(tmp_path)
    msg = make_message("just chatting")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_not_called()


def test_incoming_message_is_logged(tmp_path):
    bot = make_bot(tmp_path)
    msg = make_message("hello")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send"):
        bot.process_messages()
    log_file = tmp_path / "2025_03_15.txt"
    assert log_file.exists()
    content = log_file.read_text()
    assert "hello" in content
    assert "incoming" in content


def test_response_message_is_logged(tmp_path):
    bot = make_bot(tmp_path)
    msg = make_message("/test hello")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send"):
        bot.process_messages()
    log_files = list(tmp_path.glob("*.txt"))
    all_lines = []
    for f in sorted(log_files):
        all_lines.extend(f.read_text().strip().split("\n"))
    assert len(all_lines) == 2
    assert "incoming" in all_lines[0]
    assert "outgoing" in all_lines[1]
    assert "olleh" in all_lines[1]


def test_multiple_messages_processed(tmp_path):
    bot = make_bot(tmp_path)
    msg1 = make_message("/test abc")
    msg2 = make_message("plain message")
    msg3 = make_message("/test xyz", sender="+440002222222")
    with patch.object(bot.signal_cli, "receive", return_value=[msg1, msg2, msg3]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        assert mock_send.call_count == 2
        mock_send.assert_any_call("+440001111111", "cba")
        mock_send.assert_any_call("+440002222222", "zyx")


def test_no_messages_received(tmp_path):
    bot = make_bot(tmp_path)
    with patch.object(bot.signal_cli, "receive", return_value=[]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_not_called()


def test_unregistered_command_no_response(tmp_path):
    bot = make_bot(tmp_path)
    msg = make_message("/unknown do stuff")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_not_called()
