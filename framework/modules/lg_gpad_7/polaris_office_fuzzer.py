# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e
from os import listdir, getcwd
from random import randint, sample
from subprocess import Popen, PIPE, CalledProcessError
from blessings import Terminal
from framework.utilities.process_management import ProcessManagement
from framework.triage.utils import Utils
import time
t = Terminal()


class PolarisOfficeFuzzer(object):

    label = "lg_gpad_7_polaris_office_fuzzer"
    tag = "LG GPad 7 Polaris Office Fuzzer"

    @staticmethod
    def run():
        """
        Run target fuzzer
        :return:
        """
        logger.debug("Starting LG GPad 7 Polaris Office Fuzzer (!)")

        _test_cases = [

            "docx",
            "doc",
            "pdf",
            "ppt"
        ]

        for test_case in _test_cases:
            logger.debug("Available Test-Case : {0}".format(test_case))

        # Get target test-case
        target = raw_input(t.yellow("(DroidFuzzer) Select" + t.white(" Test-Case: ")))

        # Clear logcat before running test-cases
        ProcessManagement.clear()
        processes = list()

        # Clear existing tombstones
        Utils.clear_tombstones()

        for test_case in _test_cases:
            log_id = randint(0, 10000)
            if target == test_case:
                # Always return a random sample of the generate test-cases
                for item in sample(listdir("".join([getcwd(), "/test-cases/{0}".format(target)])),
                                   len(listdir("".join([getcwd(), "/test-cases/{0}".format(target)])))):

                    logger.debug("Fuzzing : {0}".format(item))

                    try:
                        # Push the selected test-case on to the device
                        pusher = ProcessManagement.execute("".join([getcwd(),
                                                                    "/bin/adb push ",
                                                                    "{0}/test-cases/{1}/{2}".format(getcwd(),
                                                                                                    target, item)," /sdcard/"]))
                        processes.append(pusher)
                        time.sleep(5)
                        # Execute the target parser
                        viewer = ProcessManagement.execute("".join([getcwd(),
                                                                    "/bin/adb shell su '-c am start ",
                                                                    "-n com.infraware.polarisoffice5tablet/com.infraware.filemanager.FmLauncherActivity ",
                                                                    "-d file:///storage/emulated/0/{0}'".format(item)]))
                        processes.append(viewer)
                        time.sleep(10)
                        # Log the test-case
                        log = ProcessManagement.execute(
                            "".join([getcwd(),
                                     "/bin/adb shell log -p v -t 'Filename' {0}".format(item)]))

                        processes.append(log)
                        time.sleep(3)
                        # Log any SIGSEGV
                        fatal = ProcessManagement.execute(
                            "".join([getcwd(),
                                     "/bin/adb logcat -v time *:F > ",
                                     "logs/lg_gpad_7/polaris_office/{0}/lg_gpad_7_polaris_office_{1}_{2}_logs"
                                    .format(target, item, log_id)]))

                        processes.append(fatal)
                        time.sleep(3)
                        # Log the test-case that triggered the SIGSEGV
                        logcat = ProcessManagement.execute(
                            "".join([getcwd(),
                                     "/bin/adb logcat -v time *:F -s 'Filename' > ",
                                     "logs/lg_gpad_7/polaris_office/{0}/lg_gpad_7_polaris_office_{1}_{2}_logs"
                                    .format(target, item, log_id)]))

                        processes.append(logcat)
                        time.sleep(3)
                        # Remove the selected test-case
                        remove = ProcessManagement.execute(
                            "".join([getcwd(), "/bin/adb shell su '-c rm /sdcard/{0}'".format(item)]))

                        ret = remove.wait()
                        # Make sure we have received a return code before proceeding
                        if ret:
                            processes.append(remove)
                            time.sleep(3)
                        # Kill the target parser
                        ProcessManagement.execute(
                            "".join([getcwd(), "/bin/adb shell am force-stop com.infraware.polarisoffice5tablet"]))
                        # Recursively kill all child processes
                        ProcessManagement.kill(processes)
                        ProcessManagement.clear()

                    except CalledProcessError as called_process_error:
                        raise called_process_error
                    except Exception as e:
                        # Handle this ...
                        if e.message == "[Errno 35] Resource temporarily unavailable":
                            logger.error(e.message)
