import logging
from blessings import Terminal
t = Terminal()


class GlobalLogger(object):

    @staticmethod
    def get_logger():

        logger = logging.getLogger('DroidFuzzer')
        logger.setLevel(logging.DEBUG)
        # Create handler
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # Create formatter
        formatter = logging.Formatter(t.yellow('%(asctime)s - %(levelname)s -') + t.white(' %(message)s'))
        console.setFormatter(formatter)
        # Add the handler
        logger.addHandler(console)

        return logger
