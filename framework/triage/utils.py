# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e

from subprocess import Popen, PIPE, CalledProcessError
from os import getcwd
from blessings import Terminal
t = Terminal()


class Utils(object):
    def __init__(self):
        super(Utils, self).__init__()

    @staticmethod
    def clear_tombstones():
        """
        Clear existing tombstones
        """
        try:
            # Requires root
            Popen("".join([getcwd(), "/bin/adb shell su -c 'rm /tombstones/*' "]), stdout=PIPE, shell=True)
        except CalledProcessError as called_process_error:
            raise called_process_error
