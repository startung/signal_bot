import signal
from unittest.mock import patch, MagicMock, call
from signal_bot.main import create_bot
from signal_bot.config import Config


def test_create_bot_uses_config():
    config = Config(
        phone_number="+440001111111",
        cli_path="signal-cli",
        log_dir="/tmp/test-logs",
    )
    bot = create_bot(config)
    assert bot.account == "+440001111111"
    assert bot.signal_cli._cli_parts == ["signal-cli"]
    assert str(bot.log_dir) == "/tmp/test-logs"


def test_create_bot_registers_test_app():
    config = Config(
        phone_number="+440001111111",
        cli_path="signal-cli",
        log_dir="/tmp/test-logs",
    )
    bot = create_bot(config)
    app = bot.registry.get("test")
    assert app is not None
    assert app.name == "test"


def test_create_bot_with_custom_cli_path():
    config = Config(
        phone_number="+440001111111",
        cli_path="flatpak run org.asamk.SignalCli",
        log_dir="logs",
    )
    bot = create_bot(config)
    assert bot.signal_cli._cli_parts == ["flatpak", "run", "org.asamk.SignalCli"]
