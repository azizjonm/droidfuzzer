try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e

from os import listdir, getcwd
import sys


class Tombstone(object):

    tombstone_location = None

    def __init__(self):
        # This will need to dynamically change based on the device
        # Samsung Core Prime for the time being
        self.tombstone = "/tombstone/tombstone_00"

    def create_crash(self, log, module):

        """
        Recreate crash based off the crash log entries
        """

        signal_type = "SIGSEGV"
        test_cases = list()
        test_case_paths = list()

        # We need to isolate the each test-case based on the signal type it triggered
        # Currently this will just be SIGSEGV
        # https://github.com/fuzzing/MFFA/blob/master/get_uniquecrash.py
        try:
            with open(log, "r") as f:
                lines = f.readlines()
                for count in range(0, len(lines)):
                    if signal_type in lines[count]:
                        check = count - 8
                        if check < 0:
                            diff = 8 - count
                            check = 8 - diff
                        else:
                            check = 8
                        for crash in range(1, check):
                            if "Filename" in lines[count - crash]:
                                test_case = lines[count - crash].split(":")
                                test_case = test_case[-1].rstrip("\n").rstrip("\r")
                                test_cases.append(test_case)
        except IOError:
            raise

        # We need to remote all of the irrelevant test-cases
        # TODO - Variable naming conventions should be less confusing
        for test_case_type in listdir("".join([getcwd(), "/test-cases"])):
            if test_case_type in test_cases[0].split(".")[1]:
                for t in listdir("".join([getcwd(), "/test-cases/{0}".format(test_case_type)])):
                    for test_case in test_cases:
                        if t in test_case:
                            test_case_path = "".join([getcwd(), "/test-cases/{0}/{1}".format(test_case_type, t)])
                            test_case_paths.append(test_case_path)
        try:
            from framework.modules.fuzzerfactory import FuzzerFactory
            factory_fuzzer = FuzzerFactory().get_fuzzer(module)
            if factory_fuzzer:
                logger.debug("Loading : {0}".format(factory_fuzzer.tag))
                factory_fuzzer.crash_triage(test_case_paths)
        except ImportError:
            raise


class TombstoneCollector(Tombstone):
    def __init__(self, log):
        super(Tombstone, self).__init__()
        self.log = log

    def collect(self):
        return


