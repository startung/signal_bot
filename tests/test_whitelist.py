from datetime import datetime, timezone
from unittest.mock import patch
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


def make_bot(tmp_path, allowed_senders=None):
    bot = Bot(
        account="+447786000000",
        cli_path="signal-cli",
        log_dir=tmp_path,
        allowed_senders=allowed_senders,
    )
    bot.register_app(ReverseApp())
    return bot


def test_whitelisted_sender_is_processed(tmp_path):
    bot = make_bot(tmp_path, allowed_senders=["+440001111111"])
    msg = make_message("/test hello")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_called_once_with("+440001111111", "olleh")


def test_whitelisted_sender_logged_to_standard_dir(tmp_path):
    bot = make_bot(tmp_path, allowed_senders=["+440001111111"])
    msg = make_message("hello")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send"):
        bot.process_messages()
    log_file = tmp_path / "2025_03_15.txt"
    assert log_file.exists()
    assert "hello" in log_file.read_text()


def test_unauthorized_sender_not_routed(tmp_path):
    bot = make_bot(tmp_path, allowed_senders=["+440001111111"])
    msg = make_message("/test hello", sender="+449999999999")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_not_called()


def test_unauthorized_sender_logged_to_unauthorized_dir(tmp_path):
    bot = make_bot(tmp_path, allowed_senders=["+440001111111"])
    msg = make_message("/test hello", sender="+449999999999")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send"):
        bot.process_messages()
    unauthorized_log = tmp_path / "unauthorized" / "2025_03_15.txt"
    assert unauthorized_log.exists()
    assert "+449999999999" in unauthorized_log.read_text()


def test_unauthorized_sender_not_logged_to_standard_dir(tmp_path):
    bot = make_bot(tmp_path, allowed_senders=["+440001111111"])
    msg = make_message("/test hello", sender="+449999999999")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send"):
        bot.process_messages()
    standard_log = tmp_path / "2025_03_15.txt"
    assert not standard_log.exists()


def test_empty_whitelist_allows_all(tmp_path):
    bot = make_bot(tmp_path, allowed_senders=[])
    msg = make_message("/test hello", sender="+449999999999")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_called_once_with("+449999999999", "olleh")


def test_none_whitelist_allows_all(tmp_path):
    bot = make_bot(tmp_path, allowed_senders=None)
    msg = make_message("/test hello", sender="+449999999999")
    with patch.object(bot.signal_cli, "receive", return_value=[msg]), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        mock_send.assert_called_once_with("+449999999999", "olleh")
