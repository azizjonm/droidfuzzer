# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e

from os import listdir, getcwd
from subprocess import Popen, PIPE, CalledProcessError
from blessings import Terminal
from framework.utilities.process_management import ProcessManagement
from framework.triage.utils import Utils
from random import randint, shuffle
import time
t = Terminal()


class ASUSZenFoneVideoFuzzer(object):

    label = "asus_zenfone_2e_video_fuzzer"
    tag = "ASUS ZenFone 2E Video Fuzzer"

    @staticmethod
    def run():
        """
        Run gallery fuzzer
        """
        logger.debug("Starting ASUS ZenFone 2E Video Fuzzer (!)")

        _test_cases = [

            "mp4",
            "mkv"
        ]

        for test_case in _test_cases:
            logger.debug("Available Test-Case : {0}".format(test_case))

        # Get target test-case
        target = raw_input(t.yellow("(DroidFuzzer) Select Test-Case: "))

        # Clear logcat before running test-cases
        ProcessManagement.clear()
        processes = list()

        # Clear existing tombstones
        Utils.clear_tombstones()

        for test_case in _test_cases:
            # Create random log identifier
            log_id = randint(0, 10000)
            if target == test_case:
                for item in listdir("".join([getcwd(), "/test-cases/{0}".format(target)])):
                    logger.debug("Fuzzing : {0}".format(item))
                    try:
                        # Push the test-case to the device
                        pusher = Popen("".join([getcwd(), "/bin/adb push ",
                                                "{0}/test-cases/{1}/{2}".format(getcwd(), target, item),
                                                " /sdcard/"]),
                                       shell=True)
                        processes.append(pusher)
                        time.sleep(2)
                        viewer = Popen(
                            "".join([getcwd(), "/bin/adb shell am start ",
                                     "-n com.asus.gallery/.app.MovieActivity ",
                                     "-t video/* "
                                     "-a android.intent.action.VIEW ",
                                     "-d file:///sdcard/{0}".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(viewer)
                        time.sleep(1)
                        # Add each test-case as a log entry
                        log = Popen(
                            "".join([getcwd(), "/bin/adb shell log -p v -t 'Filename' {0}".format(item)]),
                            shell=True)

                        processes.append(log)
                        time.sleep(1)
                        # Find and write fatal log entries (SIGSEGV)
                        fatal = Popen(
                            "".join([getcwd(),
                                     "/bin/adb logcat -v time *:F > ", getcwd(),
                                     "/logs/asus_zenfone_2e/movie/{0}/asus_zenfone_2e_movie_{0}_{1}_{2}_logs"
                                    .format(target, item, log_id)]),
                            shell=True)

                        processes.append(fatal)
                        time.sleep(1)
                        # Find and write test-case entry logs
                        logcat = Popen(
                            "".join([getcwd(),
                                     "/bin/adb logcat -v time *:F -s 'Filename' > ", getcwd(),
                                     "/logs/asus_zenfone_2e/movie/{0}/asus_zenfone_2e_movie_{0}_{1}_{2}_logs"
                                    .format(target, item, log_id)]),
                            shell=True)

                        processes.append(logcat)
                        time.sleep(1)
                        # Remove test-case from device
                        remove = Popen(
                            "".join([getcwd(), "/bin/adb shell rm /sdcard/{0}".format(item)]),
                            shell=True)
                        ret = remove.wait()
                        if ret:
                            processes.append(remove)
                            time.sleep(1)
                        # Kill target application process
                        Popen(
                            "".join([getcwd(), "/bin/adb shell am force-stop com.asus.gallery"]),
                            shell=True)
                        # Kill all adb processes
                        ProcessManagement.kill(processes)
                        ProcessManagement.clear()
                    except CalledProcessError as called_process_error:
                        raise called_process_error
