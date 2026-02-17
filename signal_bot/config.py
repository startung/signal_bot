import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    phone_number: str
    cli_path: str
    log_dir: str


def load_config(use_dotenv: bool = True) -> Config:
    if use_dotenv:
        load_dotenv()
    phone_number = os.environ.get("SIGNAL_PHONE_NUMBER")
    if not phone_number:
        raise ValueError("SIGNAL_PHONE_NUMBER environment variable is required")
    return Config(
        phone_number=phone_number,
        cli_path=os.environ.get("SIGNAL_CLI_PATH", "signal-cli"),
        log_dir=os.environ.get("LOG_DIR", "logs"),
    )
