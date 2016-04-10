# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e
from os import listdir, getcwd
from blessings import Terminal
from subprocess import Popen, PIPE, CalledProcessError
from framework.utilities.process_management import ProcessManagement
import time
t = Terminal()


class GalleryFuzzer(object):

    label = "kindle_fire_gallery_viewer_fuzzer"
    tag = "Kindle Fire Gallery Fuzzer"

    @staticmethod
    def run():
        """
        Run target fuzzer
        :return:
        """

        logger.debug("Starting Kindle Fire Gallery Fuzzer (!)")

        _test_cases = [

            "gif",
            "png",
            "mp4"
        ]

        for test_case in _test_cases:
            logger.debug("Available Test-Case : {0}".format(test_case))
        # Get target test-case
        target = raw_input(t.yellow("(DroidFuzzer) Select Test-Case: "))
        # Clear logcat before running through available test-cases
        ProcessManagement.clear()
        processes = list()

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
                            "".join([getcwd(), "/bin/adb shell am start ",
                                     "-n com.amazon.photos/com.amazon.gallery.thor.app.activity.ThorViewActivity ",
                                     "-d file:///data/local/tmp/{0}".format(item)]),
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
                                     "logs/kindle_fire_gallery_viewer_{0}_logs".format(target)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(fatal)
                        time.sleep(1)
                        # Find and write test-case entry logs
                        # ----------------------------------------------------------------------------------------
                        logcat = Popen(
                            "".join([getcwd(), "/bin/adb logcat -v time *:F -s 'Filename' >> ",
                                     "logs/kindle_fire_gallery_viewer_{0}_logs".format(target)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(logcat)
                        time.sleep(2)
                        # Remove test-case from device
                        # ----------------------------------------------------------------------------------
                        remove = Popen(
                            "".join([getcwd(), "/bin/adb shell rm /data/local/tmp/{0}".format(item)]),
                            stdout=PIPE,
                            shell=True)
                        processes.append(remove)
                        time.sleep(2)
                        # Kill target application process
                        # ------------------------------------------------------------------------------
                        Popen(
                            "".join([getcwd(), "/bin/adb shell am force-stop com.amazon.photos"]),
                            shell=True)
                        # Kill all adb processes
                        #
                        ProcessManagement.kill(processes)
                    except CalledProcessError as called_process_error:
                        raise called_process_error
