import json
from unittest.mock import patch, MagicMock
from signal_bot.signal_cli import SignalCli
from signal_bot.message import Direction


ACCOUNT = "+447786000000"


def make_envelope(source, timestamp_ms, message):
    return json.dumps({
        "envelope": {
            "source": source,
            "sourceNumber": source,
            "timestamp": timestamp_ms,
            "dataMessage": {
                "timestamp": timestamp_ms,
                "message": message,
            },
        }
    })


def test_send_calls_subprocess_with_correct_args():
    cli = SignalCli(account=ACCOUNT)
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        cli.send("+449999999999", "Hello!")
        mock_run.assert_called_once_with(
            ["signal-cli", "-a", ACCOUNT, "send", "-m", "Hello!", "+449999999999"],
            capture_output=True,
            text=True,
            check=True,
        )


def test_send_uses_custom_cli_path():
    cli = SignalCli(account=ACCOUNT, cli_path="flatpak run org.asamk.SignalCli")
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        cli.send("+449999999999", "Hi!")
        args = mock_run.call_args[0][0]
        assert args[:3] == ["flatpak", "run", "org.asamk.SignalCli"]


def test_receive_parses_json_into_messages():
    cli = SignalCli(account=ACCOUNT)
    output = make_envelope("+449999999999", 1700000000000, "Hello bot!")
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=output)
        messages = cli.receive()
        assert len(messages) == 1
        msg = messages[0]
        assert msg.sender == "+449999999999"
        assert msg.recipient == ACCOUNT
        assert msg.body == "Hello bot!"
        assert msg.direction == Direction.INCOMING


def test_receive_multiple_messages():
    cli = SignalCli(account=ACCOUNT)
    line1 = make_envelope("+440001111111", 1700000000000, "First")
    line2 = make_envelope("+440002222222", 1700000001000, "Second")
    output = line1 + "\n" + line2
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=output)
        messages = cli.receive()
        assert len(messages) == 2
        assert messages[0].body == "First"
        assert messages[1].body == "Second"


def test_receive_no_messages():
    cli = SignalCli(account=ACCOUNT)
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        messages = cli.receive()
        assert messages == []


def test_receive_skips_non_data_messages():
    cli = SignalCli(account=ACCOUNT)
    receipt = json.dumps({
        "envelope": {
            "source": "+449999999999",
            "timestamp": 1700000000000,
            "receiptMessage": {"type": "DELIVERY"},
        }
    })
    data = make_envelope("+449999999999", 1700000001000, "Real message")
    output = receipt + "\n" + data
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=output)
        messages = cli.receive()
        assert len(messages) == 1
        assert messages[0].body == "Real message"


def test_receive_skips_null_message_body():
    cli = SignalCli(account=ACCOUNT)
    output = make_envelope("+449999999999", 1700000000000, None)
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=output)
        messages = cli.receive()
        assert messages == []


def test_receive_sets_timestamp_from_envelope():
    cli = SignalCli(account=ACCOUNT)
    output = make_envelope("+449999999999", 1700000000000, "Timed")
    with patch("signal_bot.signal_cli.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=output)
        messages = cli.receive()
        assert messages[0].timestamp.year == 2023
