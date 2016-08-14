# Initialize output before importing any module, that can use colorama.
from .system import init_output

init_output()

from argparse import ArgumentParser
from pprint import pformat
import sys
from . import logs, types
from .shells import shell
from .conf import settings
from .corrector import get_corrected_commands
from .exceptions import EmptyCommand
from .utils import get_installation_info, get_alias
from .ui import select_command


def fix_command():
    """Fixes previous command. Used when `thefuck` called without arguments."""
    settings.init()
    with logs.debug_time('Total'):
        logs.debug(u'Run with settings: {}'.format(pformat(settings)))

        try:
            command = types.Command.from_raw_script(sys.argv[1:])
        except EmptyCommand:
            logs.debug('Empty command, nothing to do')
            return

        corrected_commands = get_corrected_commands(command)
        selected_command = select_command(corrected_commands)

        if selected_command:
            selected_command.run(command)
        else:
            sys.exit(1)


def print_alias():
    """Prints alias for current shell."""
    try:
        alias = sys.argv[2]
    except IndexError:
        alias = get_alias()

    print(shell.app_alias(alias))


def how_to_configure_alias():
    """Shows useful information about how-to configure alias.

    It'll be only visible when user type fuck and when alias isn't configured.

    """
    settings.init()
    logs.how_to_configure_alias(shell.how_to_configure())


def main():
    parser = ArgumentParser(prog='thefuck')
    version = get_installation_info().version
    parser.add_argument(
            '-v', '--version',
            action='version',
            version='The Fuck {} using Python {}'.format(
                    version, sys.version.split()[0]))
    parser.add_argument('-a', '--alias',
                        action='store_true',
                        help='[custom-alias-name] prints alias for current shell')
    parser.add_argument('command',
                        nargs='*',
                        help='command that should be fixed')
    known_args = parser.parse_args(sys.argv[1:2])

    if known_args.alias:
        print_alias()
    elif known_args.command:
        fix_command()
    else:
        parser.print_usage()
