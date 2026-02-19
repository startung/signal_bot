# Signaalbot

Signaalbot (*signaal* is the Dutch word for signal) is a lightweight, extensible Signal bot built in Python. It polls for incoming messages via [signal-cli](https://github.com/AsamK/signal-cli), routes `/command`-style messages to pluggable command apps, and logs all traffic to daily text files.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — package and project manager
- [signal-cli](https://github.com/AsamK/signal-cli) — local Signal CLI backend
- A phone number registered with Signal (or an existing account to link)

## Installation

```bash
git clone https://github.com/your-username/signaalbot.git
cd signaalbot
uv sync
cp .env.example .env
# Edit .env and set SIGNAL_PHONE_NUMBER at minimum
```

See the [[Configuration Reference]] for all available settings.

## Running the bot

```bash
# Normal mode (requires signal-cli and a configured .env)
uv run python -m signal_bot

# Interactive CLI mode — test commands without signal-cli
uv run python -m signal_bot --cli

# Enable debug logging
uv run python -m signal_bot --debug
# or set DEBUG=true in your .env / environment
```

In CLI mode, messages are simulated from a fixed fake sender (`+440000000000`). Add that number to `ALLOWED_SENDERS` in your `.env` so it isn't blocked by the whitelist.

## Built-in commands

| Command | Description |
|---|---|
| `/test <text>` | Reverses the text you send |
| `/date [city]` | Shows current date/time, optionally for a city |
| `/date set City, Country` | Saves a default city for `/date` |
| `/help` | Lists all registered commands |

## Further reading

- [[Configuration Reference]] — all `.env` variables, signal-cli setup, deployment
- [[Developing a New App]] — add your own `/command` in minutes
- [[Architecture]] — how the message flow and module system work
