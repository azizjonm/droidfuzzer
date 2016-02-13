from subprocess import Popen
import psutil
from os import getcwd


class ProcessManagement(object):

    @staticmethod
    def kill(p):
        """
        Kill all processes within process group
        :param p
        :return:
        """
        for process in p:
            try:
                parent = psutil.Process(process.pid)
                for children in parent.children(recursive=True):
                    children.kill()
                parent.kill()
            except psutil.NoSuchProcess as no_such_process:
                raise no_such_process
            except psutil.Error as error:
                raise error
        return

    @staticmethod
    def clear():
        """
        Clear logcat logs
        :return:
        """
        p = Popen("".join([getcwd(), "/bin/adb logcat -c"]), shell=True)
        psutil.Process(p.pid).kill()


