# Setup GlobalLogger
try:
    import logging
    logger = logging.getLogger('DroidFuzzer')
except ImportError as e:
    raise e

import json
from os import getcwd
from cmd2 import Cmd as DroidFuzzer
from blessings import Terminal
from framework.commands.enum import CommandEnum
t = Terminal()


class Run(DroidFuzzer):
    def __int__(self):
        DroidFuzzer.__init__(self)

    @staticmethod
    def do_fuzzer(args):
        """
        Usage: fuzzer show
        Usage: fuzzer module <module>
        """
        try:
            if len(args) < 2:
                logger.error("Not enough arguments (!)")
                logger.debug("Usage: fuzzer show")
                logger.debug("Usage: fuzzer module <module>")
                return
            else:
                if args.split()[0] == "show":
                    # Open module.config for accessing available fuzzing modules
                    with open("".join([getcwd(), CommandEnum.config_file_path])) as json_file:
                        _data = json_file.read()
                        _config = json.loads(_data.strip(" '<>()[]\"` ").replace("\'", '\"'))
                        for members, member in _config.items():
                            for module in member:
                                for module_name, fuzzers in module.items():
                                    for fuzzer in fuzzers:
                                        logger.debug("{0} : {1}".format(CommandEnum.available_module,
                                                                        "".join([module_name, " : ", fuzzer])))
                elif args.split()[0] == "module":
                    if args.split()[1]:
                        # Import about and create a new FuzzerFactory
                        from framework.modules.samsung_core_prime.fuzzer_factory import FuzzerFactory
                        _factory_fuzzer = FuzzerFactory.get_fuzzer(args.split()[1])
                        if _factory_fuzzer:
                            logger.debug("Loading : {0}".format(_factory_fuzzer.tag))
                            _factory_fuzzer.run()
                        else:
                            logger.debug("{0} (!) ".format(CommandEnum.module_does_not_exist))
                    else:
                        logger.error("Not enough arguments (!)")
                        logger.error("Usage: fuzzer module <module>")
        except ImportError:
            logger.error("Not able to import the FuzzerFactory")
        except IndexError:
            logger.error("Not enough arguments (!) ")

    @staticmethod
    def do_generate(args):
        try:
            if len(args) < 2:
                logger.error("Not enough arguments (!)")
                logger.debug("Usage: generator <file> <number_of_test_cases>")
                return
            else:
                from framework.generator.generator import Generator
                g = Generator(args.split()[0], args.split()[1])
                g.run()
        except IndexError:
            raise


