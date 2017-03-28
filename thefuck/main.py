# Initialize output before importing any module, that can use colorama.
from .system import init_output

init_output()

from pprint import pformat  # noqa: E402
import sys  # noqa: E402
from . import logs, types  # noqa: E402
from .shells import shell  # noqa: E402
from .conf import settings  # noqa: E402
from .corrector import get_corrected_commands  # noqa: E402
from .exceptions import EmptyCommand  # noqa: E402
from .ui import select_command  # noqa: E402
from .argument_parser import Parser  # noqa: E402
from .utils import get_installation_info  # noqa: E402


def fix_command(known_args):
    """Fixes previous command. Used when `thefuck` called without arguments."""
    settings.init(known_args)
    with logs.debug_time('Total'):
        logs.debug(u'Run with settings: {}'.format(pformat(settings)))
        raw_command = ([known_args.force_command] if known_args.force_command
                       else known_args.command)

        try:
            command = types.Command.from_raw_script(raw_command)
        except EmptyCommand:
            logs.debug('Empty command, nothing to do')
            return

        corrected_commands = get_corrected_commands(command)
        selected_command = select_command(corrected_commands)

        if selected_command:
            selected_command.run(command)
        else:
            sys.exit(1)


def main():
    parser = Parser()
    known_args = parser.parse(sys.argv)

    if known_args.help:
        parser.print_help()
    elif known_args.version:
        logs.version(get_installation_info().version,
                     sys.version.split()[0])
    elif known_args.command:
        fix_command(known_args)
    elif known_args.alias:
        print(shell.app_alias(known_args.alias))
    else:
        parser.print_usage()
