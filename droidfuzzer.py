from framework.commands.cmd import Run
from framework.utilities.logging.global_logger import GlobalLogger
from blessings import Terminal
import sys
t = Terminal()


if __name__ == "__main__":

    # Create GlobalLogger instance
    logger = GlobalLogger.get_logger()

    print(t.yellow("""

______           _     _______
|  _  \         (_)   | |  ___|
| | | |_ __ ___  _  __| | |_ _   _ ___________ _ __
| | | | '__/ _ \| |/ _` |  _| | | |_  /_  / _ \ '__|
| |/ /| | | (_) | | (_| | | | |_| |/ / / /  __/ |
|___/ |_|  \___/|_|\__,_\_|  \__,_/___/___\___|_|


    """))

    try:
        run = Run()
        run.prompt = t.yellow("(DroidFuzzer) ")
        run.ruler = t.yellow("-")
        run.cmdloop()
    except KeyboardInterrupt:
        sys.exit(0)
