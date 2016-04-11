# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e
from os import listdir, getcwd, path
import os
from subprocess import Popen, PIPE, CalledProcessError
from blessings import Terminal
from framework.utilities.process_management import ProcessManagement
from framework.triage.utils import Utils
import time
import sys
t = Terminal()


class DocumentViewerFuzzer(object):

    label = "samsung_core_prime_document_viewer_fuzzer"
    tag = "Samsung Core Prime Document Viewer Fuzzer"

    @staticmethod
    def run():
        """
        Run target fuzzer
        :return:
        """
        logger.debug("Starting Samsung Core Prime Document Viewer Fuzzer (!)")

        _test_cases = [

            "docx",
            "doc",
            "pdf"
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

        # Clear existing logs
        if path.isfile("".join([getcwd(), "/logs/samsung_core_prime_document_viewer_{0}_logs".format(target)])):
            logger.debug("Removing existing logs (!)")
            # Got an unresolved reference when just importing the function (?)
            os.remove("".join([getcwd(), "/logs/samsung_core_prime_document_viewer_{0}_logs".format(target)]))

        for test_case in _test_cases:
            if target == test_case:
                for item in listdir("".join([getcwd(), "/test-cases/{0}".format(target)])):
                    logger.debug("Fuzzing : {0}".format(item))
                    try:
                        # Push the test-case to the device
                        # -----------------------------------------------------------------------------
                        pusher = Popen("".join([getcwd(), "/bin/adb push ",
                                                "{0}/test-cases/{1}/{2}".format(getcwd(), target, item),
                                                " /data/local/tmp"]),
                                       stdout=PIPE,
                                       shell=True)
                        processes.append(pusher)
                        time.sleep(2)
                        viewer = Popen(
                            "".join([getcwd(), "/bin/adb shell su '-c am start ",
                                     "-n com.hancom.office.viewer/com.tf.thinkdroid.write.ni.viewer.WriteViewPlusActivity ",
                                     "-d file:///data/local/tmp/{0}'".format(item)]),
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
                            "".join([getcwd(), "/bin/adb logcat -v time *:F > ",
                                               "logs/samsung_core_prime_document_viewer_{0}_logs".format(target)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(fatal)
                        time.sleep(1)
                        # Find and write test-case entry logs
                        # ----------------------------------------------------------------------------------------
                        logcat = Popen(
                            "".join([getcwd(), "/bin/adb logcat -v time *:F -s 'Filename' >> ",
                                               "logs/samsung_core_prime_document_viewer_{0}_logs".format(target)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(logcat)
                        time.sleep(1)
                        # Remove test-case from device
                        # ----------------------------------------------------------------------------------
                        remove = Popen(
                            "".join([getcwd(), "/bin/adb shell su '-c rm /data/local/tmp/{0}'".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(remove)
                        time.sleep(1)
                        # Kill target application process
                        # ------------------------------------------------------------------------------
                        Popen(
                            "".join([getcwd(), "/bin/adb shell am force-stop com.hancom.office.viewer"]),
                            shell=True)
                        # Kill all adb processes
                        #
                        ProcessManagement.kill(processes)
                        sys.stdout.flush()
                    except CalledProcessError as called_process_error:
                        raise called_process_error

    @staticmethod
    def crash_triage(test_cases):
        """
        Attempt to recreate crash based on target test-case
        """
        # Clear logcat before running test-cases
        ProcessManagement.clear()
        processes = list()

        # Clear existing tombstones
        Utils.clear_tombstones()

        # TODO - Figure out why /data/local/tmp doesn't work here
        for test_case in test_cases:
            logger.debug("Fuzzing : {0}".format("".join(test_case.split("/")[-1])))
            try:
                # Push the test-case to the device
                # -----------------------------------------------------------------------------
                pusher = Popen("".join([getcwd(), "/bin/adb push ",
                                        test_case,
                                        " /data/local/tmp"]),
                               stdout=PIPE,
                               shell=True)
                ret = pusher.wait()
                if ret:
                    processes.append(pusher)
                time.sleep(3)
                viewer = Popen(
                    "".join([getcwd(),
                             "/bin/adb shell su -c 'am start -n com.hancom.office.viewer/com.tf.thinkdroid.write.ni.viewer.WriteViewPlusActivity -d file:///data/local/tmp/{0}'"
                            .format("".join(test_case.split("/")[-1]))]),
                    stdout=PIPE,
                    shell=True)
                ret = viewer.wait()
                if ret:
                    processes.append(viewer)
                time.sleep(1)
                # Remove test-case from device
                # ----------------------------------------------------------------------------------
                remove = Popen(
                    "".join([getcwd(), "/bin/adb shell rm /data/local/tmp/{0}".format("".join(test_case.split("/")[-1]))]),
                    stdout=PIPE,
                    shell=True)
                ret = remove.wait()
                if ret:
                    processes.append(remove)
                time.sleep(1)
                # Kill target application process
                # ------------------------------------------------------------------------------
                Popen(
                    "".join([getcwd(), "/bin/adb shell am force-stop com.hancom.office.viewer"]),
                    shell=True)
                # Kill all adb processes
                # ------------------------------------------------------------------------------
                ProcessManagement.kill(processes)
            except CalledProcessError as called_process_error:
                logger.error(called_process_error)

