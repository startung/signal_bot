import logging
import signal
import sys
import time
from datetime import datetime, timezone
from signal_bot.bot import Bot
from signal_bot.config import Config, load_config
from signal_bot.logging import log_message
from signal_bot.message import Message, Direction
from signal_bot.router import route_command
from signal_bot.apps.test_app import TestApp
from signal_bot.apps.date_app import DateApp
from signal_bot.apps.help_app import HelpApp

logger = logging.getLogger(__name__)

POLL_INTERVAL = 5
CLI_FAKE_SENDER = "+440000000000"
_running = True


def create_bot(config: Config) -> Bot:
    bot = Bot(
        account=config.phone_number,
        cli_path=config.cli_path,
        log_dir=config.log_dir,
        allowed_senders=config.allowed_senders,
    )
    bot.register_app(TestApp())
    bot.register_app(DateApp(data_dir=config.data_dir))
    bot.register_app(HelpApp(bot.registry))
    return bot


def _shutdown(signum, frame):
    global _running
    _running = False


def _cli_send(bot: Bot, recipient: str, body: str) -> None:
    print(f"[bot] {body}")
    outgoing = Message(
        sender=bot.account,
        recipient=recipient,
        body=body,
        direction=Direction.OUTGOING,
        timestamp=datetime.now(timezone.utc),
    )
    log_message(outgoing, bot.log_dir)


def run_cli(config: Config) -> None:
    logging.basicConfig(
        level=logging.DEBUG if config.debug else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    bot = create_bot(config)
    sender = CLI_FAKE_SENDER

    print(f"Signaalbot CLI — bot account: {config.phone_number}")
    print(f"Simulating messages from: {sender}")
    print("Type a message and press Enter. Ctrl+D or empty input to quit.")
    print()

    while True:
        try:
            raw = input("> ")
        except EOFError:
            print()
            break

        if not raw.strip():
            break

        msg = Message(
            sender=sender,
            recipient=bot.account,
            body=raw,
            direction=Direction.INCOMING,
            timestamp=datetime.now(timezone.utc),
        )

        if not bot._is_authorized(sender):
            unauthorized_dir = bot.log_dir / "unauthorized"
            unauthorized_dir.mkdir(parents=True, exist_ok=True)
            log_message(msg, unauthorized_dir)
            print("[unauthorized sender — message dropped]")
            continue

        log_message(msg, bot.log_dir)

        mode_response = bot._handle_mode_command(msg)
        if mode_response is not None:
            _cli_send(bot, sender, mode_response)
            continue

        response = route_command(msg.body, bot.registry, sender=sender)
        if response is None and sender in bot._modes:
            app = bot.registry.get(bot._modes[sender])
            if app is not None:
                response = app.handle(msg.body, sender=sender)

        if response is not None:
            _cli_send(bot, sender, response)

    print("Bye.")


def run(debug: bool | None = None):
    global _running
    _running = True

    config = load_config(debug=debug)
    logging.basicConfig(
        level=logging.DEBUG if config.debug else logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    bot = create_bot(config)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    logger.info("Signal bot started for %s", config.phone_number)
    logger.info("Polling every %ss. Press Ctrl+C to stop.", POLL_INTERVAL)

    while _running:
        try:
            bot.process_messages()
        except Exception as e:
            logger.error("Error processing messages: %s", e)
        time.sleep(POLL_INTERVAL)

    logger.info("Signal bot stopped.")
