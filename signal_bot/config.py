import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    phone_number: str
    cli_path: str
    log_dir: str
    allowed_senders: list[str] | None
    data_dir: str
    debug: bool = False
    signal_cli_mode: str = "subprocess"
    signal_cli_host: str = "localhost"
    signal_cli_port: int = 7583


def load_config(use_dotenv: bool = True, debug: bool | None = None) -> Config:
    if use_dotenv:
        load_dotenv()
    phone_number = os.environ.get("SIGNAL_PHONE_NUMBER")
    if not phone_number:
        raise ValueError("SIGNAL_PHONE_NUMBER environment variable is required")
    if debug is None:
        debug = os.environ.get("DEBUG", "").lower() in ("1", "true")
    return Config(
        phone_number=phone_number,
        cli_path=os.environ.get("SIGNAL_CLI_PATH", "signal-cli"),
        log_dir=os.environ.get("LOG_DIR", "logs"),
        allowed_senders=_parse_allowed_senders(os.environ.get("ALLOWED_SENDERS", "")),
        data_dir=os.environ.get("DATA_DIR", "data"),
        debug=debug,
        signal_cli_mode=os.environ.get("SIGNAL_CLI_MODE", "subprocess"),
        signal_cli_host=os.environ.get("SIGNAL_CLI_HOST", "localhost"),
        signal_cli_port=int(os.environ.get("SIGNAL_CLI_PORT", "7583")),
    )


def _parse_allowed_senders(value: str) -> list[str] | None:
    stripped = value.strip()
    if not stripped:
        return None
    return [s.strip() for s in stripped.split(",") if s.strip()]
