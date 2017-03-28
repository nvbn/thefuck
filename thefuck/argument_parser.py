import sys
from argparse import ArgumentParser
from .const import ARGUMENT_PLACEHOLDER
from .utils import get_alias


class Parser(object):
    def __init__(self):
        self._parser = ArgumentParser(prog='thefuck', add_help=False)
        self._parser.add_argument(
            '-v', '--version',
            action='store_true',
            help="show program's version number and exit")
        self._parser.add_argument(
            '-a', '--alias',
            nargs='?',
            const=get_alias(),
            help='[custom-alias-name] prints alias for current shell')
        self._parser.add_argument(
            '-h', '--help',
            action='store_true',
            help='show this help message and exit')
        self._parser.add_argument(
            '-y', '--yes',
            action='store_true',
            help='execute fixed command without confirmation')
        self._parser.add_argument(
            '-d', '--debug',
            action='store_true',
            help='enable debug output')
        self._parser.add_argument('command',
                                  nargs='*',
                                  help='command that should be fixed')

    def _get_arguments(self, argv):
        if ARGUMENT_PLACEHOLDER in argv:
            index = argv.index(ARGUMENT_PLACEHOLDER)
            return argv[index + 1:] + ['--'] + argv[:index]
        elif argv and not argv[0].startswith('-') and argv[0] != '--':
            return ['--'] + argv
        else:
            return argv

    def parse(self, argv):
        arguments = self._get_arguments(argv[1:])
        return self._parser.parse_args(arguments)

    def print_usage(self):
        self._parser.print_usage(sys.stderr)

    def print_help(self):
        self._parser.print_help(sys.stderr)
