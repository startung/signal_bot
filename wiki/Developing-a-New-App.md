# Developing a New App

Any new `/command` can be added with a single file in `signal_bot/apps/` and one line in `signal_bot/main.py`. No changes to the core bot are required.

## The `CommandApp` interface

All apps must subclass `CommandApp` (defined in `signal_bot/app_interface.py`) and implement three members:

| Member | Type | Description |
|---|---|---|
| `name` | `str` property | The command keyword without `/`. E.g. `"weather"` registers `/weather`. Must be unique across all registered apps. |
| `description` | `str` property | A short description shown by `/help`. |
| `handle(args, sender)` | method | Called when the command is received. `args` is everything after the command keyword; `sender` is the caller's phone number. Must return a `str` response. |

## Step 1: Create the app file

Place your app in `signal_bot/apps/your_app.py`:

```python
from signal_bot.app_interface import CommandApp

class YourApp(CommandApp):
    @property
    def name(self) -> str:
        return "yourcommand"

    @property
    def description(self) -> str:
        return "A short description of what /yourcommand does"

    def handle(self, args: str, sender: str = "") -> str:
        # args   — everything the user typed after /yourcommand
        # sender — the sender's phone number (useful for per-user state)
        return f"You said: {args}"
```

## Step 2: Register the app

In `signal_bot/main.py`, import your app and add it to `create_bot()`:

```python
from signal_bot.apps.your_app import YourApp

def create_bot(config: Config) -> Bot:
    ...
    bot.register_app(YourApp())
    ...
```

Your `/yourcommand` is now live and will appear in `/help` automatically.

## Mode support

Mode support is built into the bot — no extra code is needed in your app. Users can send `/yourcommand start` to enter a persistent mode where all subsequent plain-text messages (without a `/` prefix) are forwarded directly to your app's `handle()` method. They exit with `/yourcommand end`.

Mode state is stored in memory and resets when the bot restarts.

## Persistence

If your app needs to save state across restarts, accept a `data_dir` parameter and manage your own JSON file. The `DateApp` is the reference implementation:

```python
import json
from pathlib import Path
from signal_bot.app_interface import CommandApp

class YourApp(CommandApp):
    def __init__(self, data_dir: Path | str | None = None) -> None:
        self._data_dir = Path(data_dir) if data_dir is not None else None
        self._state: dict = self._load()

    def _state_path(self) -> Path | None:
        if self._data_dir is None:
            return None
        return self._data_dir / "your_app.json"

    def _load(self) -> dict:
        path = self._state_path()
        if path is None or not path.exists():
            return {}
        with open(path) as f:
            return json.load(f)

    def _save(self) -> None:
        path = self._state_path()
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self._state, f)
    ...
```

Then register it in `main.py` with `YourApp(data_dir=config.data_dir)`.

## Testing

Tests live in `tests/`. The project follows TDD — write tests before the implementation. Use `pytest`'s `tmp_path` fixture for any app that writes files.

```bash
uv run pytest tests/test_your_app.py -v
```
