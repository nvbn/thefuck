from argparse import ArgumentParser
from warnings import warn
from pathlib import Path
from os.path import expanduser
from pprint import pformat
import pkg_resources
import sys
import colorama
from . import logs, types, shells
from .conf import initialize_settings_file, init_settings, settings
from .corrector import get_corrected_commands
from .exceptions import EmptyCommand
from .ui import select_command


def setup_user_dir():
    """Returns user config dir, create it when it doesn't exist."""
    user_dir = Path(expanduser('~/.thefuck'))
    rules_dir = user_dir.joinpath('rules')
    if not rules_dir.is_dir():
        rules_dir.mkdir(parents=True)
    initialize_settings_file(user_dir)
    return user_dir


# Entry points:

def fix_command():
    colorama.init()
    user_dir = setup_user_dir()
    init_settings(user_dir)
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


def _get_current_version():
    return pkg_resources.require('thefuck')[0].version


def print_alias(entry_point=True):
    if entry_point:
        warn('`thefuck-alias` is deprecated, use `thefuck --alias` instead.')
        position = 1
    else:
        position = 2

    alias = shells.thefuck_alias()
    if len(sys.argv) > position:
        alias = sys.argv[position]
    print(shells.app_alias(alias))


def how_to_configure_alias():
    """Shows useful information about how-to configure alias.

    It'll be only visible when user type fuck and when alias isn't configured.

    """
    colorama.init()
    user_dir = setup_user_dir()
    init_settings(user_dir)
    logs.how_to_configure_alias(shells.how_to_configure())


def main():
    parser = ArgumentParser(prog='thefuck')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {}'.format(_get_current_version()))
    parser.add_argument('-a', '--alias',
                        action='store_true',
                        help='[custom-alias-name] prints alias for current shell')
    parser.add_argument('command',
                        nargs='*',
                        help='command that should be fixed')
    known_args = parser.parse_args(sys.argv[1:2])
    if known_args.alias:
        print_alias(False)
    elif known_args.command:
        fix_command()
    else:
        parser.print_usage()
