"""Module with shell specific actions, each shell class should
implement `from_shell`, `to_shell`, `app_alias` and `put_to_history`
methods.

"""
from collections import defaultdict
from subprocess import Popen, PIPE
from time import time
import os
from psutil import Process
from .utils import DEVNULL


class Generic(object):
    def _get_aliases(self):
        return {}

    def _expand_aliases(self, command_script):
        aliases = self._get_aliases()
        binary = command_script.split(' ')[0]
        if binary in aliases:
            return command_script.replace(binary, aliases[binary], 1)
        else:
            return command_script

    def from_shell(self, command_script):
        """Prepares command before running in app."""
        return self._expand_aliases(command_script)

    def to_shell(self, command_script):
        """Prepares command for running in shell."""
        return command_script

    def app_alias(self):
        return "\nalias fuck='eval $(thefuck $(fc -ln -1))'\n"

    def _get_history_file_name(self):
        return ''

    def _get_history_line(self, command_script):
        return ''

    def put_to_history(self, command_script):
        """Puts command script to shell history."""
        history_file_name = self._get_history_file_name()
        if os.path.isfile(history_file_name):
            with open(history_file_name, 'a') as history:
                history.write(self._get_history_line(command_script))


class Bash(Generic):
    def _parse_alias(self, alias):
        name, value = alias.replace('alias ', '', 1).split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    def _get_aliases(self):
        proc = Popen('bash -ic alias', stdout=PIPE, stderr=DEVNULL, shell=True)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.bash_history'))

    def _get_history_line(self, command_script):
        return u'{}\n'.format(command_script)


class Zsh(Generic):
    def _parse_alias(self, alias):
        name, value = alias.split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    def _get_aliases(self):
        proc = Popen('zsh -ic alias', stdout=PIPE, stderr=DEVNULL, shell=True)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.zsh_history'))

    def _get_history_line(self, command_script):
        return u': {}:0;{}\n'.format(int(time()), command_script)


shells = defaultdict(lambda: Generic(), {
    'bash': Bash(),
    'zsh': Zsh()})


def _get_shell():
    shell = Process(os.getpid()).parent().cmdline()[0]
    return shells[shell]


def from_shell(command):
    return _get_shell().from_shell(command)


def to_shell(command):
    return _get_shell().to_shell(command)


def app_alias():
    return _get_shell().app_alias()


def put_to_history(command):
    return _get_shell().put_to_history(command)
