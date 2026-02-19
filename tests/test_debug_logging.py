import logging
import pytest
from signal_bot.config import load_config
from signal_bot.registry import AppRegistry
from signal_bot.router import route_command
from signal_bot.app_interface import CommandApp


class EchoApp(CommandApp):
    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Echoes text"

    def handle(self, args: str, sender: str = "") -> str:
        return args


# --- Config: debug flag ---

def test_debug_false_by_default(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.delenv("DEBUG", raising=False)
    config = load_config(use_dotenv=False)
    assert config.debug is False


def test_debug_true_from_env_var(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.setenv("DEBUG", "true")
    config = load_config(use_dotenv=False)
    assert config.debug is True


def test_debug_true_from_env_var_1(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.setenv("DEBUG", "1")
    config = load_config(use_dotenv=False)
    assert config.debug is True


def test_debug_override_arg_takes_precedence(monkeypatch):
    monkeypatch.setenv("SIGNAL_PHONE_NUMBER", "+440001111111")
    monkeypatch.delenv("DEBUG", raising=False)
    config = load_config(use_dotenv=False, debug=True)
    assert config.debug is True


# --- Router: debug log messages ---

def test_router_logs_debug_on_known_command(caplog):
    registry = AppRegistry()
    registry.register(EchoApp())
    with caplog.at_level(logging.DEBUG, logger="signal_bot.router"):
        route_command("/echo hello", registry, sender="+441111111111")
    assert any("echo" in r.message for r in caplog.records)


def test_router_logs_debug_on_unknown_command(caplog):
    registry = AppRegistry()
    with caplog.at_level(logging.DEBUG, logger="signal_bot.router"):
        route_command("/unknown stuff", registry)
    assert any("unknown" in r.message for r in caplog.records)


def test_router_no_debug_log_for_non_command(caplog):
    registry = AppRegistry()
    with caplog.at_level(logging.DEBUG, logger="signal_bot.router"):
        route_command("just a plain message", registry)
    assert not caplog.records
