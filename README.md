# 🤖 Signal Bot

A lightweight, extensible Signal bot built in Python. It sends and receives messages, logs everything, and routes `/command`-style messages to pluggable apps.

## ✨ Features

- **Send & receive** Signal messages
- **Command routing** — messages starting with `/command` are dispatched to registered apps
- **Message logging** — all incoming and outgoing messages are logged
- **Extensible** — add new command apps independently without touching the core bot

## 📦 Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for package and project management
- [signal-cli](https://github.com/AsamK/signal-cli) installed locally
- A phone number to register with Signal (or an existing Signal account to link)

## 🚀 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/signal-bot.git
cd signal-bot

# Install dependencies with uv
uv sync
```

## 📡 signal-cli Setup

This project uses [signal-cli](https://github.com/AsamK/signal-cli) as a local binary to send and receive Signal messages via subprocess calls.

### 1. Install signal-cli

**Option A — Flatpak (recommended for development):**

```bash
flatpak install flathub org.asamk.SignalCli
```

> 💡 When using the Flatpak version, set `SIGNAL_CLI_PATH` to `flatpak run org.asamk.SignalCli` in your `.env` file.

**Option B — Standalone binary (recommended for production):**

Download the latest release from the [signal-cli releases page](https://github.com/AsamK/signal-cli/releases) and extract it:

```bash
# Download and extract (replace VERSION with the latest version)
wget https://github.com/AsamK/signal-cli/releases/download/v0.13.12/signal-cli-0.13.12-Linux.tar.gz
tar xf signal-cli-0.13.12-Linux.tar.gz -C /opt/
sudo ln -s /opt/signal-cli-0.13.12/bin/signal-cli /usr/local/bin/signal-cli
```

> 📋 **Note:** The standalone binary requires Java (JRE 21+). Install it with `sudo apt install openjdk-21-jre-headless` if needed.

### 2. Register a new phone number

```bash
signal-cli -a +YOUR_PHONE_NUMBER register
```

> ⚠️ **Captcha required?** Visit https://signalcaptchas.org/registration/generate.html, solve it, copy the `signalcaptcha://...` token, and add `--captcha 'signalcaptcha://...'` to the register command.

```bash
# Verify with the SMS code you receive
signal-cli -a +YOUR_PHONE_NUMBER verify 123-456
```

### 2b. Or link to an existing Signal account

```bash
signal-cli link -n "signal-cli-bot"
```

This prints a `sgnl://linkdevice?...` URI. Convert it to a QR code (e.g. `qrencode -t ANSI`) and scan it from the Signal app on your phone.

### 3. Verify it's working

```bash
# Send a test message
signal-cli -a +YOUR_PHONE_NUMBER send -m "Hello from signal-cli!" +RECIPIENT_NUMBER

# Receive messages
signal-cli -a +YOUR_PHONE_NUMBER receive
```

## ⚙️ Configuration

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `SIGNAL_PHONE_NUMBER` | The phone number registered to your bot |
| `SIGNAL_CLI_PATH` | Path to signal-cli binary (default: `signal-cli`) |

## 🏃 Usage

```bash
# Run the bot
uv run python -m signal_bot

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/test_something.py::test_specific_function -v
```

## 🔧 Commands

Commands are messages that start with `/` followed by a keyword. The bot routes them to the matching registered app.

| Command | App | Description |
|---|---|---|
| `/test` | Test App | Reverses the text you send (e.g. `/test hello` → `olleh`) |
| `/date` | Date App | Shows current date/time. Use `/date London` for a city, `/date set Tokyo, JP` to save a default |
| `/help` | Help App | Lists all available commands and their descriptions |

> 💡 **Adding your own command app:** Implement the command app interface, register it with the bot, and your new `/command` is ready to go. Each app is a standalone module — no changes to the core bot required.

## 🏗️ Architecture

```
signal_bot/
├── bot.py          # Core bot: message send/receive loop
├── commands/       # Command router and app registry
├── logging/        # Message logging
└── apps/           # Pluggable command apps (e.g. todo)
```

**How it works:**

1. The bot listens for incoming Signal messages
2. Every message (in and out) is logged
3. If a message starts with `/`, the command router looks up the registered app
4. The matched app processes the command and returns a response
5. The bot sends the response back via Signal

## 🧪 Testing

This project follows **test-driven development (TDD)**. Tests live in the `tests/` directory.

```bash
# Run the full test suite
uv run pytest

# Run with verbose output
uv run pytest -v

# Run tests matching a keyword
uv run pytest -k "test_command"
```

## 🚢 Deployment

### Running as a systemd service

1. Create a service file:

```ini
# /etc/systemd/system/signal-bot.service
[Unit]
Description=Signal Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/signal-bot
ExecStart=/path/to/.local/bin/uv run python -m signal_bot
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start:

```bash
sudo systemctl enable signal-bot
sudo systemctl start signal-bot
```

3. Check logs:

```bash
journalctl -u signal-bot -f
```

> 🛡️ **Tip:** Run the bot on a Raspberry Pi or a cheap VPS for a low-cost always-on setup.

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
