# Development Plan

This document tracks the development roadmap for Signaalbot. Each step will be implemented using test-driven development (TDD): write tests first, then implement to make them pass.

## Steps

1. **Project initialisation** - Set up the Python project with `uv`, create `pyproject.toml`, configure pytest, and establish the package structure (`signal_bot/`, `tests/`).

2. **Message model** - Define a `Message` data class representing a Signal message (sender, recipient, body, timestamp, direction in/out).

3. **Message logging** - Implement a logger that records every message (incoming and outgoing) with timestamp and metadata.

4. **Command parser** - Build a parser that detects `/command` messages, extracts the command name, and separates any arguments from the body.

5. **App interface** - Define the base interface (abstract class / protocol) that all command apps must implement, establishing the contract for receiving a command and returning a response.

6. **App registry** - Create a registry where command apps are registered by their `/command` name and looked up at dispatch time.

7. **Command router** - Wire the command parser to the app registry so that incoming `/command` messages are dispatched to the correct app and responses are returned.

8. **Signal backend integration** - Integrate with signal-cli (or equivalent) to send and receive real Signal messages.

9. **Bot core / main loop** - Build the main bot loop that ties everything together: receive → log → route → respond → log.

10. **Configuration** - Load settings from environment variables / `.env` file (phone number, signal-cli path, log level, etc.).

11. **Todo app (example command app)** - Implement a `/todo` app as the first plugin to validate the extensibility model.

12. **Deployment setup** - Add systemd service file, document production deployment, and handle graceful shutdown.

13. **Sender whitelist** - Only process messages from a configurable list of allowed phone numbers. Messages from unknown senders are ignored (and optionally logged).

14. **Mode switching** - Allow a sender to enter a command app's "mode" with `/command start` so that all subsequent messages are routed to that app without a prefix, until `/command end` exits the mode.

15. **Date app** - A simple `/date` command app that returns the current date and time.

16. **Help app** - A `/help` command app that lists all registered commands and their descriptions.

17. **Persistent date defaults** - Persist `/date set` defaults to a JSON file in a configurable `DATA_DIR` so they survive restarts.

18. **CLI testing interface** - An interactive REPL mode (`--cli` flag) for testing the bot without signal-cli, simulating messages from a fake sender.

19. **Debug logging** - Integrate Python stdlib `logging` throughout the codebase. Each module gets its own `logging.getLogger(__name__)` logger. Enabled via `--debug` CLI flag or `DEBUG=true` env var (added to `Config`). Logs key internal events: message receipt, skipped envelopes, authorization checks, command dispatch, mode transitions, and missing responses. Log level is `DEBUG` when enabled, `WARNING` otherwise.

20. **GitHub wiki** - Create a `wiki/` directory with four Markdown files matching GitHub wiki conventions (pushable to `<repo>.wiki.git`): `Home.md` (overview, install, quick start), `Developing-a-New-App.md` (CommandApp interface, mode support, persistence pattern), `Configuration-Reference.md` (all `.env` variables, signal-cli setup, systemd deployment), and `Architecture.md` (message flow, module responsibilities, mode system).

21. **Docker support** - Add a `Dockerfile` for signaalbot and a `docker-compose.yml` that runs signaalbot alongside signal-cli as a sidecar service. signal-cli runs in daemon mode (JSON-RPC or stdio) so signaalbot can communicate with it over the network or a shared socket. Volumes for signal-cli account data, message logs, and app data. Configuration via the existing `.env` file. Update the wiki Configuration Reference with Docker deployment instructions.

## Status Key

- ⬜ Not started
- 🟡 In progress
- ✅ Complete

## Progress

| # | Step | Status |
|---|---|---|
| 1 | Project initialisation | ✅ |
| 2 | Message model | ✅ |
| 3 | Message logging | ✅ |
| 4 | Command parser | ✅ |
| 5 | App interface | ✅ |
| 6 | App registry | ✅ |
| 7 | Command router | ✅ |
| 8 | Signal backend integration | ✅ |
| 9 | Bot core / main loop | ✅ |
| 10 | Configuration | ✅ |
| 11 | Test app (example command app) | ✅ |
| 12 | Deployment setup | ✅ |
| | **v1.0.0 release** | 🎉 |
| 13 | Sender whitelist | ✅ |
| 14 | Mode switching | ✅ |
| 15 | Date app | ✅ |
| 16 | Help app | ✅ |
| | **v1.1.0 release** | 🎉 |
| 17 | Persistent date defaults | ✅ |
| | **v1.1.1 release** | 🎉 |
| 18 | CLI testing interface | ✅ |
| | **v1.2.0 release** | 🎉 |
| 19 | Debug logging | ✅ |
| 20 | GitHub wiki | ✅ |
| | **v1.3.0 release** | 🎉 |
| | **v1.3.1 release** | 🎉 |
| | **v1.3.2 release** | 🎉 |
| 21 | Docker support | ⬜ |
