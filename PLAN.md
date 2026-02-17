# Development Plan

This document tracks the development roadmap for Signal Bot. Each step will be implemented using test-driven development (TDD): write tests first, then implement to make them pass.

## Steps

1. **Project initialisation** — Set up the Python project with `uv`, create `pyproject.toml`, configure pytest, and establish the package structure (`signal_bot/`, `tests/`).

2. **Message model** — Define a `Message` data class representing a Signal message (sender, recipient, body, timestamp, direction in/out).

3. **Message logging** — Implement a logger that records every message (incoming and outgoing) with timestamp and metadata.

4. **Command parser** — Build a parser that detects `/command` messages, extracts the command name, and separates any arguments from the body.

5. **App interface** — Define the base interface (abstract class / protocol) that all command apps must implement, establishing the contract for receiving a command and returning a response.

6. **App registry** — Create a registry where command apps are registered by their `/command` name and looked up at dispatch time.

7. **Command router** — Wire the command parser to the app registry so that incoming `/command` messages are dispatched to the correct app and responses are returned.

8. **Signal backend integration** — Integrate with signal-cli (or equivalent) to send and receive real Signal messages.

9. **Bot core / main loop** — Build the main bot loop that ties everything together: receive → log → route → respond → log.

10. **Configuration** — Load settings from environment variables / `.env` file (phone number, signal-cli path, log level, etc.).

11. **Todo app (example command app)** — Implement a `/todo` app as the first plugin to validate the extensibility model.

12. **Deployment setup** — Add systemd service file, document production deployment, and handle graceful shutdown.

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
