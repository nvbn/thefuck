from argparse import ArgumentParser
from warnings import warn
from pathlib import Path
from os.path import expanduser
from pprint import pformat
import pkg_resources
from subprocess import Popen, PIPE
import os
import sys
from psutil import Process, TimeoutExpired
import colorama
import six
from . import logs, types, shells
from .conf import initialize_settings_file, init_settings, settings
from .corrector import get_corrected_commands
from .utils import compatibility_call
from .ui import select_command


def setup_user_dir():
    """Returns user config dir, create it when it doesn't exist."""
    user_dir = Path(expanduser('~/.thefuck'))
    rules_dir = user_dir.joinpath('rules')
    if not rules_dir.is_dir():
        rules_dir.mkdir(parents=True)
    initialize_settings_file(user_dir)
    return user_dir


def wait_output(popen):
    """Returns `True` if we can get output of the command in the
    `settings.wait_command` time.

    Command will be killed if it wasn't finished in the time.

    """
    proc = Process(popen.pid)
    try:
        proc.wait(settings.wait_command)
        return True
    except TimeoutExpired:
        for child in proc.children(recursive=True):
            child.kill()
        proc.kill()
        return False


def get_command(args):
    """Creates command from `args` and executes it."""
    if six.PY2:
        script = ' '.join(arg.decode('utf-8') for arg in args[1:])
    else:
        script = ' '.join(args[1:])

    script = script.strip()
    if not script:
        return

    script = shells.from_shell(script)
    env = dict(os.environ)
    env.update(settings.env)

    with logs.debug_time(u'Call: {}; with env: {};'.format(script, env)):
        result = Popen(script, shell=True, stdout=PIPE, stderr=PIPE, env=env)
        if wait_output(result):
            stdout = result.stdout.read().decode('utf-8')
            stderr = result.stderr.read().decode('utf-8')

            logs.debug(u'Received stdout: {}'.format(stdout))
            logs.debug(u'Received stderr: {}'.format(stderr))

            return types.Command(script, stdout, stderr)
        else:
            logs.debug(u'Execution timed out!')
            return types.Command(script, None, None)


def run_command(old_cmd, command):
    """Runs command from rule for passed command."""
    if command.side_effect:
        compatibility_call(command.side_effect, old_cmd, command.script)
    shells.put_to_history(command.script)
    print(command.script)


# Entry points:

def fix_command():
    colorama.init()
    user_dir = setup_user_dir()
    init_settings(user_dir)
    with logs.debug_time('Total'):
        logs.debug(u'Run with settings: {}'.format(pformat(settings)))

        command = get_command(sys.argv)

        if not command:
            logs.debug('Empty command, nothing to do')
            return

        corrected_commands = get_corrected_commands(command)
        selected_command = select_command(corrected_commands)
        if selected_command:
            run_command(command, selected_command)


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
