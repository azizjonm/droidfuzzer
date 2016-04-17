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
from random import randint
import time
t = Terminal()


class ThinkfreeDocumentFuzzer(object):

    label = "thinkfree_document_fuzzer"
    tag = "Thinkfree Document Fuzzer"

    @staticmethod
    def run():
        """
        Run gallery fuzzer
        """
        logger.debug("Starting Thinkfree Document Fuzzer (!)")

        _test_cases = [

            "doc",
            "docx"
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

            log_id = randint(0, 10000)

            if target == test_case:
                for item in listdir("".join([getcwd(), "/test-cases/{0}".format(target)])):
                    logger.debug("Fuzzing : {0}".format(item))
                    try:
                        # Push the test-case to the device
                        # -----------------------------------------------------------------------------
                        pusher = Popen("".join([getcwd(), "/bin/adb push ",
                                                "{0}/test-cases/{1}/{2}".format(getcwd(), target, item),
                                                " /sdcard/"]),
                                       stdout=PIPE,
                                       shell=True)
                        processes.append(pusher)
                        time.sleep(2)
                        viewer = Popen(
                            "".join([getcwd(), "/bin/adb shell am start ",
                                     "-n com.tf.thinkdroid.amlite/com.tf.thinkdroid.write.viewer.HdWriteViewerActivity ",
                                     "-t application/vnd.openxmlformats-officedocument.wordprocessingml.document "
                                     "-a android.intent.action.VIEW ",
                                     "-d file:///sdcard/{0}".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(viewer)
                        time.sleep(1)
                        # Add each test-case as a log entry
                        # -------------------------------------------------------------------------------
                        log = Popen(
                            "".join([getcwd(), "/bin/adb shell log -p v -t 'Filename' {0}".format(item)]),
                            stdout=PIPE,
                            shell=True)

                        processes.append(log)
                        time.sleep(1)
                        # Find and write fatal log entries (SIGSEGV)
                        # ----------------------------------------------------------------------------------------
                        fatal = Popen(
                            "".join([getcwd(),
                                     "/bin/adb logcat -v time *:F > ", getcwd(),
                                     "/logs/thinkfree/document/{0}/thinkfree_document_{0}_{1}_{2}_logs"
                                    .format(target, item, log_id)]),
                            stdout=PIPE,
                            shell=True)

                        processes.append(fatal)
                        time.sleep(1)
                        # Find and write test-case entry logs
                        # ----------------------------------------------------------------------------------------
                        logcat = Popen(
                            "".join([getcwd(),
                                     "/bin/adb logcat -v time *:F -s 'Filename' > ", getcwd(),
                                     "/logs/thinkfree/document/{0}/thinkfree_document_{0}_{1}_{2}_logs"
                                    .format(target, item, log_id)]),
                            stdout=PIPE,
                            shell=True)

                        processes.append(logcat)
                        time.sleep(1)
                        # Remove test-case from device
                        # ----------------------------------------------------------------------------------
                        remove = Popen(
                            "".join([getcwd(), "/bin/adb shell rm /sdcard/{0}".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        ret = remove.wait()
                        if ret:
                            processes.append(remove)
                            time.sleep(1)
                        # Kill target application process
                        # ------------------------------------------------------------------------------
                        Popen(
                            "".join([getcwd(), "/bin/adb shell am force-stop com.tf.thinkdroid.amlite"]),
                            stdout=PIPE,
                            shell=True)
                        # Kill all adb processes
                        ProcessManagement.kill(processes)
                        ProcessManagement.clear()
                    except CalledProcessError as called_process_error:
                        raise called_process_error
