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
        Clear logcat logs
        :return:
        """
        p = Popen("".join([getcwd(), "/bin/adb logcat -c"]), shell=True)
        ret = p.wait()
        if ret:
            psutil.Process(p.pid).kill()


