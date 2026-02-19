# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.1.0] - 2026-02-19

### Added
- `todo_app.py` - a `/todo` command app that manages a todo list. Developed seperately [signaal\_todo](https://github.com/startung/signaal_todo)

## [2.0.2] - 2026-02-19

### Added
- Docker Hub descriptions for `startung/signaalbot` and `startung/signal-cli` (`docker/hub-signaalbot.md`, `docker/hub-signal-cli.md`)
- GitHub Actions workflow now syncs Docker Hub descriptions automatically on version tag push

## [2.0.1] - 2026-02-19

### Fixed
- signal-cli Docker image updated to v0.13.24 with Linux-native binary (no Java required)
- Switch base image from `eclipse-temurin:21-jre-jammy` to `debian:bookworm-slim`

## [2.0.0] - 2026-02-19

### Added
- Docker Compose deployment with signaalbot and signal-cli as separate containers
- `signal_cli_jsonrpc.py` - JSON-RPC over TCP backend for communicating with signal-cli daemon
- `Dockerfile` for signaalbot and `docker/signal-cli/Dockerfile` for signal-cli
- GitHub Actions workflow to automatically build and push both images to Docker Hub on version tag
- `SIGNAL_CLI_MODE`, `SIGNAL_CLI_HOST`, `SIGNAL_CLI_PORT` config options for selecting the backend
- Pre-built images published to Docker Hub (`startung/signaalbot`, `startung/signal-cli`)

## [1.3.2] - 2026-02-19

### Changed
- GitHub username updated to `startung` across README, wiki, and CLAUDE.md

## [1.3.1] - 2026-02-19

### Changed
- README trimmed to quick-start essentials; detailed docs moved to GitHub wiki
- Wiki Home page updated to match README structure, including CLI mode example

## [1.3.0] - 2026-02-19

### Added
- Debug logging via Python stdlib `logging` throughout the codebase; enabled with `--debug` flag or `DEBUG=true` env var
- `debug` field added to `Config`; log level is `DEBUG` when enabled, `WARNING` otherwise
- Key events logged: message receipt, skipped envelopes, authorization drops, command routing, mode transitions, missing responses
- GitHub wiki source in `wiki/` - four pages covering Home, Developing a New App, Configuration Reference, and Architecture

## [1.2.0] - 2026-02-19

### Added
- CLI testing interface (`--cli` flag) - interactive REPL for testing the bot without signal-cli running
- `CLI_FAKE_SENDER` constant (`+440000000000`) used as the simulated sender in CLI mode
- CLI mode logs all messages (incoming and outgoing) to `LOG_DIR` the same as normal operation

## [1.1.1] - 2026-02-18

### Added
- Persistent `/date set` defaults - saved to `DATA_DIR/date_defaults.json` and restored on startup
- `DATA_DIR` config option for persistent app data (default: `data`)

## [1.1.0] - 2026-02-18

### Added
- Sender whitelist via `ALLOWED_SENDERS` env var - unauthorized messages logged separately to `logs/unauthorized/`
- Mode switching: `/command start` enters a mode routing all plain messages to that app, `/command end` exits
- `/date` command app - shows date/time for a city, supports per-sender defaults via `/date set City, Country`
- `/help` command app - lists all registered commands and their descriptions
- `description` property added to `CommandApp` interface
- `sender` parameter added to `CommandApp.handle()` interface for per-user state
- `all_apps()` method on `AppRegistry` to list registered apps

## [1.0.0] - 2026-02-17

### Added
- CHANGELOG.md to track project changes
- CLAUDE.md for AI pair programming guidance
- README.md with installation, usage, commands, architecture, testing, and deployment docs
- PLAN.md with 12-step development roadmap
- Project initialisation: pytest dev dependency, `signal_bot/` package, `tests/` directory, smoke test
- `Message` dataclass with sender, recipient, body, timestamp, and `Direction` enum (incoming/outgoing)
- File-based message logging with daily log files (`YYYY_MM_DD.txt`), appending all messages per day
- Command parser with `ParsedCommand` dataclass, extracts command name and args from `/command` messages
- `CommandApp` abstract base class with `name` property and `handle(args) -> str` method
- `AppRegistry` with `register(app)` and `get(command_name)` methods, duplicate detection
- Command router wiring parser → registry → app dispatch via `route_command(body, registry)`
- README: signal-cli setup guide (Flatpak and standalone binary options, registration, linking)
- `SignalCli` backend class wrapping signal-cli subprocess calls for send and receive with JSON parsing
- `Bot` core class tying together receive → log → route → respond → log via `process_messages()`
- Configuration module with `.env` support via python-dotenv, `.env.example` template
- `/test` command app - reverses text arguments as a proof of extensibility
- Main entrypoint with polling loop, graceful shutdown (SIGINT/SIGTERM), `__main__.py` module support
- `systemd/signal-bot.service` template for production deployment
