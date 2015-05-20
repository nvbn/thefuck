"""Module with shell specific actions, each shell class should
implement `from_shell`, `to_shell`, `app_alias`, `put_to_history` and `get_aliases`
methods.

"""
from collections import defaultdict
from subprocess import Popen, PIPE
from time import time
import os
from psutil import Process
from .utils import DEVNULL


class Generic(object):
    def get_aliases(self):
        return {}

    def _expand_aliases(self, command_script):
        aliases = self.get_aliases()
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

    def and_(self, *commands):
        return ' && '.join(commands)


class Bash(Generic):
    def app_alias(self):
        return "\nalias fuck='eval $(thefuck $(fc -ln -1)); history -r'\n"

    def _parse_alias(self, alias):
        name, value = alias.replace('alias ', '', 1).split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    def get_aliases(self):
        proc = Popen('bash -ic alias', stdout=PIPE, stderr=DEVNULL, shell=True)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias and '=' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.bash_history'))

    def _get_history_line(self, command_script):
        return u'{}\n'.format(command_script)


class Fish(Generic):
    def app_alias(self):
        return ("function fuck -d 'Correct your previous console command'\n"
                "    set -l exit_code $status\n"
                "    set -l eval_script"
                " (mktemp 2>/dev/null ; or mktemp -t 'thefuck')\n"
                "    set -l fucked_up_commandd $history[1]\n"
                "    thefuck $fucked_up_commandd > $eval_script\n"
                "    . $eval_script\n"
                "    rm $eval_script\n"
                "    if test $exit_code -ne 0\n"
                "        history --delete $fucked_up_commandd\n"
                "    end\n"
                "end")

    def _get_history_file_name(self):
        return os.path.expanduser('~/.config/fish/fish_history')

    def _get_history_line(self, command_script):
        return u'- cmd: {}\n   when: {}\n'.format(command_script, int(time()))

    def and_(self, *commands):
        return '; and '.join(commands)


class Zsh(Generic):
    def app_alias(self):
        return "\nalias fuck='eval $(thefuck $(fc -ln -1 | tail -n 1)); fc -R'\n"

    def _parse_alias(self, alias):
        name, value = alias.split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    def get_aliases(self):
        proc = Popen('zsh -ic alias', stdout=PIPE, stderr=DEVNULL, shell=True)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias and '=' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.zsh_history'))

    def _get_history_line(self, command_script):
        return u': {}:0;{}\n'.format(int(time()), command_script)


class Tcsh(Generic):
    def app_alias(self):
        return "\nalias fuck 'set fucked_cmd=`history -h 2 | head -n 1` && eval `thefuck ${fucked_cmd}`'\n"

    def _parse_alias(self, alias):
        name, value = alias.split("\t", 1)
        return name, value

    def get_aliases(self):
        proc = Popen('tcsh -ic alias', stdout=PIPE, stderr=DEVNULL, shell=True)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias and '\t' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.history'))

    def _get_history_line(self, command_script):
        return u'#+{}\n{}\n'.format(int(time()), command_script)


shells = defaultdict(lambda: Generic(), {
    'bash': Bash(),
    'fish': Fish(),
    'zsh': Zsh(),
    'csh': Tcsh(),
    'tcsh': Tcsh()})


def _get_shell():
    try:
        shell = Process(os.getpid()).parent().name()
    except TypeError:
        shell = Process(os.getpid()).parent.name
    return shells[shell]


def from_shell(command):
    return _get_shell().from_shell(command)


def to_shell(command):
    return _get_shell().to_shell(command)


def app_alias():
    print(_get_shell().app_alias())


def put_to_history(command):
    return _get_shell().put_to_history(command)


def and_(*commands):
    return _get_shell().and_(*commands)


def get_aliases():
    return _get_shell().get_aliases().keys()
