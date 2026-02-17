from dataclasses import dataclass


@dataclass
class ParsedCommand:
    command: str
    args: str


def parse_command(body: str) -> ParsedCommand | None:
    stripped = body.strip()
    if not stripped.startswith("/") or len(stripped) < 2:
        return None
    parts = stripped[1:].split(None, 1)
    command = parts[0]
    args = parts[1].strip() if len(parts) > 1 else ""
    return ParsedCommand(command=command, args=args)
