from pathlib import Path
from signal_bot.message import Message


def log_message(message: Message, log_dir: Path) -> None:
    filename = message.timestamp.strftime("%Y_%m_%d") + ".txt"
    log_file = Path(log_dir) / filename
    timestamp = message.timestamp.isoformat()
    line = f"{timestamp} [{message.direction.value}] {message.sender} -> {message.recipient}: {message.body}\n"
    with open(log_file, "a") as f:
        f.write(line)
