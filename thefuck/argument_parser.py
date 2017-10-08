import sys
from argparse import ArgumentParser, SUPPRESS
from .const import ARGUMENT_PLACEHOLDER
from .utils import get_alias


class Parser(object):
    """Argument parser that can handle arguments with our special
    placeholder.

    """

    def __init__(self):
        self._parser = ArgumentParser(prog='thefuck', add_help=False)
        self._add_arguments()

    def _add_arguments(self):
        """Adds arguments to parser."""
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
            '-l', '--shell-logger',
            action='store',
            help='log shell output to the file')
        self._parser.add_argument(
            '--enable-experimental-instant-mode',
            action='store_true',
            help='enable experimental instant mode, use on your own risk')
        self._parser.add_argument(
            '-h', '--help',
            action='store_true',
            help='show this help message and exit')
        self._add_conflicting_arguments()
        self._parser.add_argument(
            '-d', '--debug',
            action='store_true',
            help='enable debug output')
        self._parser.add_argument(
            '--force-command',
            action='store',
            help=SUPPRESS)
        self._parser.add_argument(
            'command',
            nargs='*',
            help='command that should be fixed')

    def _add_conflicting_arguments(self):
        """It's too dangerous to use `-y` and `-r` together."""
        group = self._parser.add_mutually_exclusive_group()
        group.add_argument(
            '-y', '--yes',
            action='store_true',
            help='execute fixed command without confirmation')
        group.add_argument(
            '-r', '--repeat',
            action='store_true',
            help='repeat on failure')

    def _prepare_arguments(self, argv):
        """Prepares arguments by:

        - removing placeholder and moving arguments after it to beginning,
          we need this to distinguish arguments from `command` with ours;

        - adding `--` before `command`, so our parse would ignore arguments
          of `command`.

        """
        if ARGUMENT_PLACEHOLDER in argv:
            index = argv.index(ARGUMENT_PLACEHOLDER)
            return argv[index + 1:] + ['--'] + argv[:index]
        elif argv and not argv[0].startswith('-') and argv[0] != '--':
            return ['--'] + argv
        else:
            return argv

    def parse(self, argv):
        arguments = self._prepare_arguments(argv[1:])
        return self._parser.parse_args(arguments)

    def print_usage(self):
        self._parser.print_usage(sys.stderr)

    def print_help(self):
        self._parser.print_help(sys.stderr)
