# 🤖 Signaalbot

> **Not a typo!** *Signaal* is the Dutch word for signal.

A lightweight, extensible Signal bot built in Python. It sends and receives messages, logs everything, and routes `/command`-style messages to pluggable apps.

## ✨ Features

- **Send & receive** Signal messages
- **Command routing** - messages starting with `/command` are dispatched to registered apps
- **Message logging** - all incoming and outgoing messages are logged
- **Extensible** - add new command apps independently without touching the core bot

## 📦 Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for package and project management
- [signal-cli](https://github.com/AsamK/signal-cli) installed and configured
- A phone number registered with Signal (or an existing Signal account to link)

## 🐳 Deploy with Docker (recommended)

Pre-built images are available on Docker Hub. You only need Docker and the compose file:

```bash
curl -O https://raw.githubusercontent.com/startung/signaalbot/main/docker-compose.yml
```

Create a `.env` file with at minimum:
```
SIGNAL_PHONE_NUMBER=+YOUR_PHONE_NUMBER
ALLOWED_SENDERS=+YOUR_NUMBER
```

Then follow the [Docker deployment guide](https://github.com/startung/signaalbot/wiki/Configuration-Reference#deployment-with-docker-compose) in the wiki for signal-cli registration and startup.

## 🚀 Install from source

```bash
git clone https://github.com/startung/signaalbot.git
cd signaalbot
uv sync
cp .env.example .env
```

Set `SIGNAL_PHONE_NUMBER` in `.env` to the phone number registered to your bot. See the [Configuration Reference](https://github.com/startung/signaalbot/wiki/Configuration-Reference) wiki page for all options, signal-cli setup, and deployment.

## 🏃 Usage

```bash
# Run the bot
uv run python -m signal_bot

# Run in CLI mode (no signal-cli required - useful for testing)
uv run python -m signal_bot --cli

# Enable debug logging
uv run python -m signal_bot --debug
```

### CLI mode

The `--cli` flag starts an interactive REPL for testing command routing without signal-cli running. Messages are simulated from a fixed fake sender (`+440000000000`) - add it to `ALLOWED_SENDERS` in `.env` so it isn't blocked by the whitelist.

```
Signaalbot CLI - bot account: +441234567890
Simulating messages from: +440000000000
Type a message and press Enter. Ctrl+D or empty input to quit.

> /help
[bot] Available commands: ...
> /date start
[bot] Entered date mode. ...
> London
[bot] London: Thursday 2026-02-19 10:30:00 GMT
> /date end
[bot] Exited date mode.
```

## 🔧 Commands

| Command | Description | Source |
|---|---|---|
| `/test <text>` | Reverses the text you send | |
| `/date [city]` | Shows current date/time, optionally for a city | |
| `/date set City, Country` | Saves a default city for `/date` | |
| `/help` | Lists all registered commands | |
| `/todo <cmd>` | Manages a todo list | [signaal\_todo](https://github.com/startung/signaal_todo) |

## 🧪 Testing

```bash
uv run pytest
uv run pytest -v
uv run pytest -k "test_command"
```

## 📖 Wiki

Full documentation is available in the [wiki](https://github.com/startung/signaalbot/wiki):

- [Home](https://github.com/startung/signaalbot/wiki/Home) - overview and quick start
- [Configuration Reference](https://github.com/startung/signaalbot/wiki/Configuration-Reference) - all settings, signal-cli setup, deployment
- [Developing a New App](https://github.com/startung/signaalbot/wiki/Developing-a-New-App) - add your own `/command` in minutes
- [Architecture](https://github.com/startung/signaalbot/wiki/Architecture) - how the message flow and module system work

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
