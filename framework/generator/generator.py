# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e
from os import path, getcwd, makedirs, listdir
from subprocess import Popen, CalledProcessError, PIPE
from blessings import Terminal
t = Terminal()


class Generator(object):

    def __init__(self, sample, number):
        super(Generator, self).__init__()
        self.sample = sample
        self.number = number

    def run(self):
        """
        Generate test-cases
        :return:
        """

        for s in listdir("".join([getcwd(), "/samples/"])):
            if self.sample == s.split(".")[1]:
                print(s.split(".")[1])
                try:
                    logger.debug("Generating Test-Cases from Sample : {0}".format(self.sample))
                    if path.exists("".join([getcwd(), "/test-cases/{0}".format(self.sample)])):
                        logger.debug("Already generated Test-Cases from Sample : {0}".format(self.sample))
                    else:
                        makedirs("".join([getcwd(), "/test-cases/{0}".format(self.sample)]))
                    # TODO - Provide more control over radamsa usage
                    # TODO - Handle specific mutation control for different file formats
                    Popen(
                        "".join([
                            getcwd(),
                            "/bin/radamsa -v -n {0} -o {1} {2}"
                                .format(self.number,
                                        "".join([getcwd(),
                                                 "/test-cases/{0}/test-case-%n.{0}".format(self.sample)]),
                                        "".join([getcwd(), "/samples/", s]))]), stdout=PIPE, shell=True).wait()
                except CalledProcessError:
                    raise
                except IOError:
                    raise
