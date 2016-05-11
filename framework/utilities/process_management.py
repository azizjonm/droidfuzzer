from subprocess import Popen, PIPE
import psutil
from os import getcwd


class ProcessManagement(object):

    @staticmethod
    def kill(p):
        """
        Recursively kill all child processes for a given parent process
        """
        for process in p:
            try:
                parent = psutil.Process(process.pid)
                if parent.is_running():
                    for children in parent.children(recursive=True):
                        children.kill()
                    parent.kill()
            except psutil.NoSuchProcess:
                continue
            except psutil.Error as error:
                raise error
        return

    @staticmethod
    def clear():
        """
        Clear logs and kill the logcat process
        """
        p = Popen("".join([getcwd(), "/bin/adb logcat -c"]), shell=True)
        ret = p.wait()
        if ret:
            psutil.Process(p.pid).kill()

    @staticmethod
    def execute(cmd):
        """
        Execute command and return the process
        """
        # https://docs.python.org/3/library/subprocess.html
        # It is import to use close_fds or you will routinely run into the "[Errno 24] Too many open files" error
        p = Popen(cmd, stdout=PIPE, shell=True, close_fds=True)
        return p



