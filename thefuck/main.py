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
from . import logs, conf, types, shells
from .corrector import get_corrected_commands
from .ui import select_command


def setup_user_dir():
    """Returns user config dir, create it when it doesn't exist."""
    user_dir = Path(expanduser('~/.thefuck'))
    rules_dir = user_dir.joinpath('rules')
    if not rules_dir.is_dir():
        rules_dir.mkdir(parents=True)
    conf.initialize_settings_file(user_dir)
    return user_dir


def wait_output(settings, popen):
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


def get_command(settings, args):
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

    with logs.debug_time(u'Call: {}; with env: {};'.format(script, env),
                         settings):
        result = Popen(script, shell=True, stdout=PIPE, stderr=PIPE, env=env)
        if wait_output(settings, result):
            stdout = result.stdout.read().decode('utf-8')
            stderr = result.stderr.read().decode('utf-8')

            logs.debug(u'Received stdout: {}'.format(stdout), settings)
            logs.debug(u'Received stderr: {}'.format(stderr), settings)

            return types.Command(script, stdout, stderr)
        else:
            logs.debug(u'Execution timed out!', settings)
            return types.Command(script, None, None)


def run_command(old_cmd, command, settings):
    """Runs command from rule for passed command."""
    if command.side_effect:
        command.side_effect(old_cmd, command.script, settings)
    shells.put_to_history(command.script)
    print(command.script)


# Entry points:

def fix_command():
    colorama.init()
    user_dir = setup_user_dir()
    settings = conf.get_settings(user_dir)
    with logs.debug_time('Total', settings):
        logs.debug(u'Run with settings: {}'.format(pformat(settings)), settings)

        command = get_command(settings, sys.argv)

        if not command:
            logs.debug('Empty command, nothing to do', settings)
            return

        corrected_commands = get_corrected_commands(command, user_dir, settings)
        selected_command = select_command(corrected_commands, settings)
        if selected_command:
            run_command(command, selected_command, settings)


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


def main():
    parser = ArgumentParser(prog='The Fuck')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {}'.format(
                            pkg_resources.require('thefuck')[0].version))
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
