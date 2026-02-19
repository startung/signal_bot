# Configuration Reference

## Environment variables

All configuration is read from environment variables, optionally loaded from a `.env` file at startup. Copy `.env.example` to get started:

```bash
cp .env.example .env
```

| Variable | Default | Required | Description |
|---|---|---|---|
| `SIGNAL_PHONE_NUMBER` | — | Yes | The phone number registered to the bot (E.164 format, e.g. `+441234567890`) |
| `SIGNAL_CLI_PATH` | `signal-cli` | No | Path or command used to invoke signal-cli. Use `flatpak run org.asamk.SignalCli` for Flatpak installs. |
| `LOG_DIR` | `logs` | No | Directory where daily message log files are written. Created automatically if it doesn't exist. |
| `DATA_DIR` | `data` | No | Directory where apps store persistent data (e.g. `/date` defaults). Created automatically if it doesn't exist. |
| `ALLOWED_SENDERS` | (all allowed) | No | Comma-separated list of phone numbers allowed to use the bot. Leave empty to allow all senders. Messages from unlisted numbers are logged to `LOG_DIR/unauthorized/` and dropped. |
| `DEBUG` | `false` | No | Set to `true` or `1` to enable DEBUG-level logging. Can also be enabled at runtime with the `--debug` flag. |

## signal-cli setup

### Option A: Flatpak (easiest for development)

```bash
flatpak install flathub org.asamk.SignalCli
```

Set in `.env`:
```
SIGNAL_CLI_PATH=flatpak run org.asamk.SignalCli
```

### Option B: Standalone binary (recommended for production)

Download the latest release from the [signal-cli releases page](https://github.com/AsamK/signal-cli/releases):

```bash
wget https://github.com/AsamK/signal-cli/releases/download/v0.13.12/signal-cli-0.13.12-Linux.tar.gz
tar xf signal-cli-0.13.12-Linux.tar.gz -C /opt/
sudo ln -s /opt/signal-cli-0.13.12/bin/signal-cli /usr/local/bin/signal-cli
```

The standalone binary requires Java (JRE 21+):
```bash
sudo apt install openjdk-21-jre-headless
```

### Register a new phone number

```bash
signal-cli -a +YOUR_PHONE_NUMBER register
# If a captcha is required, visit https://signalcaptchas.org/registration/generate.html
# and append --captcha 'signalcaptcha://...' to the command above

signal-cli -a +YOUR_PHONE_NUMBER verify 123-456
```

### Link to an existing Signal account

```bash
signal-cli link -n "signaalbot"
# Prints a sgnl://linkdevice?... URI — convert to QR code and scan from the Signal app
# qrencode -t ANSI 'sgnl://linkdevice?...'
```

### Verify signal-cli is working

```bash
signal-cli -a +YOUR_PHONE_NUMBER send -m "Hello from signal-cli!" +RECIPIENT_NUMBER
signal-cli -a +YOUR_PHONE_NUMBER receive
```

## Deployment as a systemd service

### 1. Create the service file

```ini
# /etc/systemd/system/signaalbot.service
[Unit]
Description=Signaalbot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/signaalbot
EnvironmentFile=/path/to/signaalbot/.env
ExecStart=/home/your-user/.local/bin/uv run python -m signal_bot
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable signaalbot
sudo systemctl start signaalbot
```

### 3. Check logs

```bash
journalctl -u signaalbot -f
```
