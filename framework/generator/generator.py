# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e
from os import path, getcwd, makedirs, error
from subprocess import Popen, CalledProcessError
from blessings import Terminal
t = Terminal()


class Generator(object):

    def __init__(self, file_path, number):
        super(Generator, self).__init__()
        self.file_path = file_path
        self.number = number

    def run(self):
        """
        Generate test-cases
        :return:
        """
        # Get the file extension from the file path
        ext = path.splitext(self.file_path)[1]

        if path.exists("".join([getcwd(), "/test-cases/{0}".format(ext.strip("."))])):
            logger.debug("Extension already exists (!)")
            logger.debug("Generating Test-Cases (!)")
        else:
            # Create a directory for the extension if it doesn't already exist
            logger.debug("Creating directory for the {0} extension (!)".format(ext))
            try:
                makedirs("".join([getcwd(), "/test-cases/{0}".format(ext.strip("."))]))
            except error:
                raise
        try:
            # TODO - Provide more control over radamsa usage
            Popen(
                "".join([
                    getcwd(),
                    "/bin/radamsa -p od -m ft=2,fo=2,fn,num=3,td,tr2,ts1 -v -n {0} -o {1} {2}"
                        .format(self.number,
                                "".join([getcwd(), "/test-cases/{0}/test-case-%n.{0}".format(ext.strip("."))]),
                                self.file_path)]), shell=True).wait()
        except CalledProcessError:
            raise

