import sys
from signal_bot.main import run, run_cli
from signal_bot.config import load_config

if "--cli" in sys.argv:
    run_cli(load_config())
else:
    run()
