# Architecture

## Message flow

```
signal-cli (subprocess)
       │
       ▼
  SignalCli.receive()          signal_bot/signal_cli.py
       │  parses JSON → list[Message]
       ▼
  Bot.process_messages()       signal_bot/bot.py
       │
       ├─ _is_authorized(sender)?  ──No──▶ log to unauthorized/ and drop
       │
       ├─ log_message(incoming)    signal_bot/logging.py
       │
       ├─ _handle_mode_command()   mode start/end detection
       │       └─ if mode command → send confirmation, done
       │
       ├─ route_command()          signal_bot/router.py
       │       └─ parse_command()  signal_bot/parser.py
       │           └─ registry.get(command) → app.handle(args, sender)
       │
       ├─ (if no command match and sender is in a mode)
       │       └─ active_app.handle(body, sender)
       │
       └─ _send_response() if response
               ├─ SignalCli.send()        signal_bot/signal_cli.py
               └─ log_message(outgoing)  signal_bot/logging.py
```

## Module responsibilities

| Module | Responsibility |
|---|---|
| `signal_cli.py` | Wraps `signal-cli` subprocess calls. `receive()` parses NDJSON output into `Message` objects; `send()` dispatches outgoing messages. |
| `message.py` | `Message` dataclass (sender, recipient, body, direction, timestamp) and `Direction` enum. |
| `parser.py` | `parse_command(body)` — detects `/command args` syntax and returns a `ParsedCommand(command, args)` or `None`. |
| `registry.py` | `AppRegistry` — maps command names to `CommandApp` instances. Raises `ValueError` on duplicate registration. |
| `router.py` | `route_command(body, registry, sender)` — calls the parser and dispatches to the matched app. Returns `None` for non-commands or unknown commands. |
| `app_interface.py` | `CommandApp` abstract base class that all apps must subclass. |
| `bot.py` | `Bot` — top-level orchestrator. Owns `SignalCli`, `AppRegistry`, the mode state dict, and the log directory. |
| `logging.py` | `log_message(message, log_dir)` — appends a timestamped line to a daily `.txt` file. |
| `config.py` | `Config` dataclass + `load_config()` — reads `.env` and environment variables. |
| `main.py` | `create_bot()`, `run()`, `run_cli()` — wires everything together and starts the poll loop or interactive CLI. |

## Mode system

Mode is an in-memory per-sender state stored in `Bot._modes: dict[str, str]` (sender phone number → command name).

- `/command start` — if `command` is a registered app, sets `_modes[sender] = command` and confirms to the user.
- `/command end` — if `_modes[sender] == command`, removes the entry and confirms.
- While in mode, plain-text messages (no `/` prefix) bypass the router and go directly to the active app's `handle()`.
- Mode state is **not persisted** — it resets when the bot restarts.

## Persistence pattern

Apps that need state across restarts accept a `data_dir: Path | str | None` constructor argument and manage their own JSON file inside it. The directory is created lazily on first write. `DateApp` (in `signal_bot/apps/date_app.py`) is the canonical example.

The `DATA_DIR` env var is passed as `config.data_dir` to any app that needs it when `create_bot()` is called in `main.py`.

## Logging

Two separate logging mechanisms co-exist:

| Mechanism | Purpose | Module |
|---|---|---|
| Message logging | Records every incoming/outgoing `Message` to daily `.txt` files in `LOG_DIR` | `signal_bot/logging.py` |
| Debug logging | Python stdlib `logging` at `DEBUG`/`WARNING` level throughout the codebase; enabled with `--debug` or `DEBUG=true` | All modules via `logging.getLogger(__name__)` |

## Adding a new module

The core bot (`bot.py`, `router.py`, `main.py`) does not need to change when adding a new app. The only required touch point is registering the new app in `create_bot()` in `main.py`. See [[Developing a New App]] for the full walkthrough.
