import os
import pytest
from signal_bot.config import load_config


def test_loads_phone_number_from_env(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    config = load_config(use_dotenv=False)
    assert config.phone_number == "+440001111111"


def test_loads_cli_path_from_env(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.setenv("SIGNAL_CLI_PATH", "flatpak run org.asamk.SignalCli")
    config = load_config(use_dotenv=False)
    assert config.cli_path == "flatpak run org.asamk.SignalCli"


def test_cli_path_defaults_to_signal_cli(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.delenv("SIGNAL_CLI_PATH", raising=False)
    config = load_config(use_dotenv=False)
    assert config.cli_path == "signal-cli"


def test_loads_log_dir_from_env(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.setenv("LOG_DIR", "/var/log/signal-bot")
    config = load_config(use_dotenv=False)
    assert config.log_dir == "/var/log/signal-bot"


def test_log_dir_defaults_to_logs(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.delenv("LOG_DIR", raising=False)
    config = load_config(use_dotenv=False)
    assert config.log_dir == "logs"


def test_missing_phone_number_raises_error(monkeypatch):
    monkeypatch.delenv("SIGNAL_PHONE_NUMBER", raising=False)
    with pytest.raises(ValueError, match="SIGNAL_PHONE_NUMBER"):
        load_config(use_dotenv=False)
