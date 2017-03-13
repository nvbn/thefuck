# Initialize output before importing any module, that can use colorama.
from .system import init_output

init_output()

from argparse import ArgumentParser  # noqa: E402
from pprint import pformat  # noqa: E402
import sys  # noqa: E402
from . import logs, types  # noqa: E402
from .shells import shell  # noqa: E402
from .conf import settings  # noqa: E402
from .corrector import get_corrected_commands  # noqa: E402
from .exceptions import EmptyCommand  # noqa: E402
from .utils import get_installation_info, get_alias  # noqa: E402
from .ui import select_command  # noqa: E402


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


def main():
    parser = ArgumentParser(prog='thefuck')
    version = get_installation_info().version
    parser.add_argument('-v', '--version',
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
