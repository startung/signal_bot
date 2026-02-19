import sys
from signal_bot.main import run, run_cli
from signal_bot.config import load_config

_debug = "--debug" in sys.argv

if "--cli" in sys.argv:
    run_cli(load_config(debug=_debug))
else:
    run(debug=_debug)
