import json
from collections.abc import Iterator
from pathlib import Path

import httpx
import ollama

# Use the top line for dev and the second when moving to the production environment
#from app_interface import CommandApp
from signal_bot.app_interface import CommandApp

MODEL = "gemma3:12b-it-qat"


class Gemma3App(CommandApp):
    def __init__(self, data_dir: str | None = None, ollama_host: str = "http://localhost:11434"):
        self.data_dir = Path(data_dir)
        self._client = ollama.Client(host=ollama_host)

    @property
    def name(self) -> str:
        return "gemma3"

    @property
    def description(self) -> str:
        return "Have a discussion with a locally hosted instance of Gemma3"

    def _history_file(self, sender: str):
        return self.data_dir / "gemma3" / f"{sender}.json"

    def _load_history(self, sender: str) -> list:
        f = self._history_file(sender)
        if f.exists():
            return json.loads(f.read_text())
        return []

    def _save_history(self, sender: str, history: list) -> None:
        f = self._history_file(sender)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(history))

    def handle(self, args: str, sender: str = "") -> Iterator[str]:
        command = args.strip().lower()

        if command == "help":
            yield "Commands: help, clear"
            yield "Anything else is sent to Gemma3 as a message."
            return

        if command == "clear":
            f = self._history_file(sender)
            if f.exists():
                f.unlink()
            yield "Conversation history cleared."
            return

        history = self._load_history(sender)
        history.append({"role": "user", "content": args})

        full_response = ""
        current_line = ""

        try:
            for chunk in self._client.chat(model=MODEL, messages=list(history), stream=True):
                text = chunk.message.content
                full_response += text
                current_line += text

                while "\n" in current_line:
                    line, current_line = current_line.split("\n", 1)
                    if line.strip():
                        yield line
        except httpx.ConnectError:
            yield "Gemma3 is unavailable. Is ollama running?"
            return

        if current_line.strip():
            yield current_line

        history.append({"role": "assistant", "content": full_response})
        self._save_history(sender, history)
