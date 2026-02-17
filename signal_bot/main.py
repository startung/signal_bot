import signal
import sys
import time
from signal_bot.bot import Bot
from signal_bot.config import Config, load_config
from signal_bot.apps.test_app import TestApp

POLL_INTERVAL = 5
_running = True


def create_bot(config: Config) -> Bot:
    bot = Bot(
        account=config.phone_number,
        cli_path=config.cli_path,
        log_dir=config.log_dir,
    )
    bot.register_app(TestApp())
    return bot


def _shutdown(signum, frame):
    global _running
    _running = False


def run():
    global _running
    _running = True

    config = load_config()
    bot = create_bot(config)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    print(f"Signal bot started for {config.phone_number}")
    print(f"Polling every {POLL_INTERVAL}s. Press Ctrl+C to stop.")

    while _running:
        try:
            bot.process_messages()
        except Exception as e:
            print(f"Error processing messages: {e}", file=sys.stderr)
        time.sleep(POLL_INTERVAL)

    print("Signal bot stopped.")
