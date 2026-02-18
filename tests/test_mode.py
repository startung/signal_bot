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

    def handle(self, args: str, sender: str = "") -> str:
        return args[::-1]


class EchoApp(CommandApp):
    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Echoes text"

    def handle(self, args: str, sender: str = "") -> str:
        return args


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
    bot.register_app(EchoApp())
    return bot


def process(bot, messages):
    with patch.object(bot.signal_cli, "receive", return_value=messages), \
         patch.object(bot.signal_cli, "send") as mock_send:
        bot.process_messages()
        return mock_send


def test_start_activates_mode(tmp_path):
    bot = make_bot(tmp_path)
    mock_send = process(bot, [make_message("/test start")])
    mock_send.assert_called_once()
    assert "+440001111111" in bot._modes


def test_start_sends_confirmation(tmp_path):
    bot = make_bot(tmp_path)
    mock_send = process(bot, [make_message("/test start")])
    response = mock_send.call_args[0][1]
    assert "test" in response.lower()


def test_plain_messages_routed_in_mode(tmp_path):
    bot = make_bot(tmp_path)
    process(bot, [make_message("/test start")])
    mock_send = process(bot, [make_message("hello, world!")])
    mock_send.assert_called_once_with("+440001111111", "!dlrow ,olleh")


def test_end_deactivates_mode(tmp_path):
    bot = make_bot(tmp_path)
    process(bot, [make_message("/test start")])
    mock_send = process(bot, [make_message("/test end")])
    mock_send.assert_called_once()
    assert "+440001111111" not in bot._modes


def test_end_sends_confirmation(tmp_path):
    bot = make_bot(tmp_path)
    process(bot, [make_message("/test start")])
    mock_send = process(bot, [make_message("/test end")])
    response = mock_send.call_args[0][1]
    assert "test" in response.lower()


def test_plain_messages_not_routed_after_end(tmp_path):
    bot = make_bot(tmp_path)
    process(bot, [make_message("/test start")])
    process(bot, [make_message("/test end")])
    mock_send = process(bot, [make_message("hello, world!")])
    mock_send.assert_not_called()


def test_other_commands_work_in_mode(tmp_path):
    bot = make_bot(tmp_path)
    process(bot, [make_message("/test start")])
    mock_send = process(bot, [make_message("/echo hi there")])
    mock_send.assert_called_once_with("+440001111111", "hi there")


def test_independent_sender_modes(tmp_path):
    bot = make_bot(tmp_path)
    process(bot, [make_message("/test start", sender="+440001111111")])
    # Sender A is in test mode, sender B is not
    mock_send = process(bot, [make_message("hello", sender="+440002222222")])
    mock_send.assert_not_called()
    mock_send = process(bot, [make_message("hello", sender="+440001111111")])
    mock_send.assert_called_once_with("+440001111111", "olleh")


def test_start_unknown_command_not_activated(tmp_path):
    bot = make_bot(tmp_path)
    mock_send = process(bot, [make_message("/unknown start")])
    mock_send.assert_not_called()
    assert "+440001111111" not in bot._modes
