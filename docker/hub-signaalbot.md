# Signaalbot

*Signaal* is the Dutch word for signal.

A lightweight, extensible Signal bot built in Python. It polls for incoming messages via [signal-cli](https://github.com/AsamK/signal-cli), routes `/command`-style messages to pluggable command apps, and logs all traffic to daily text files.

## Quick start

You only need Docker and a phone number registered with Signal.

```bash
curl -O https://raw.githubusercontent.com/startung/signaalbot/main/docker-compose.yml
```

Create a `.env` file:

```
SIGNAL_PHONE_NUMBER=+YOUR_PHONE_NUMBER
ALLOWED_SENDERS=+YOUR_NUMBER
```

Register with Signal (one-time):

```bash
docker compose run --rm signal-cli -a +YOUR_PHONE_NUMBER register
docker compose run --rm signal-cli -a +YOUR_PHONE_NUMBER verify 123-456
```

Start the bot:

```bash
docker compose up -d
```

## Built-in commands

| Command | Description |
|---|---|
| `/test <text>` | Reverses the text you send |
| `/date [city]` | Shows current date/time, optionally for a city |
| `/date set City, Country` | Saves a default city for `/date` |
| `/help` | Lists all registered commands |

## Configuration

Key environment variables:

| Variable | Default | Description |
|---|---|---|
| `SIGNAL_PHONE_NUMBER` | - | Phone number registered with Signal (required) |
| `ALLOWED_SENDERS` | - | Comma-separated list of phone numbers allowed to send commands (required) |
| `LOG_DIR` | `logs` | Directory for message logs |
| `DATA_DIR` | `data` | Directory for persistent app data |

See the [Configuration Reference](https://github.com/startung/signaalbot/wiki/Configuration-Reference) for the full list of options.

## Links

- [Source code](https://github.com/startung/signaalbot)
- [Wiki](https://github.com/startung/signaalbot/wiki)
- [signal-cli image](https://hub.docker.com/r/startung/signal-cli)
