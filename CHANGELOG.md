# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
- `/test` command app — reverses text arguments as a proof of extensibility
- Main entrypoint with polling loop, graceful shutdown (SIGINT/SIGTERM), `__main__.py` module support
- `systemd/signal-bot.service` template for production deployment
