# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e

from os import walk, getcwd, listdir
from framework.triage.tombstone import Tombstone, TombstoneCollector


class Triage(object):
    def __init__(self):
        super(Triage, self).__init__()

    def logs(self):
        """
        Return available crash logs for triage
        """

        # This is tight and clean as fuck (!)
        try:
            for root in listdir("".join([getcwd(), "/logs"])):
                module = (next(walk("".join([getcwd(), "/logs/{0}".format(root)]))))
                if module:
                    types = (next(walk("".join([getcwd(), "/logs/{0}/{1}".format(root, module[1][0])]))))
                    if types:
                        for t in types[1]:
                            logger.debug("Available Logs : {0}".format("".join(["/",
                                                                                module[0].split("/")[-1],
                                                                                "/",
                                                                                module[1][0],
                                                                                "/",
                                                                                t])))
        except IOError:
            logger.error("Logs Unavailable (!)")

    def run(self, log, module):
        """
        Triage target crash log
        """
        path = None

        try:
            if log:
                # Create the fully qualified path to the crash log
                path = "".join([getcwd(), "/logs/{0}".format(log)])
        except IOError:
            raise

        # We need to recreate the crash based on the crash log entries
        logger.debug("Triaging : {0}".format(log))
        tombstone = Tombstone()
        tombstone.generate_unique_crash(path, module)

    def collect(self, log, module):
        """
        Collect tombstones from unique crash
        """
        path = None

        try:
            if log:
                # Create the fully qualified path to the crash log
                path = "".join([getcwd(), "/logs/{0}".format(log)])
        except IOError:
            raise

        # We need to recreate the crash based on the crash log entries
        logger.debug("Collecting : {0}".format(log))
        collector = TombstoneCollector(path, module)
        collector.collect()

