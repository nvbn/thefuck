"""Module with shell specific actions, each shell class should
implement `from_shell`, `to_shell`, `app_alias`, `put_to_history` and `get_aliases`
methods.

"""
from collections import defaultdict
from psutil import Process
from subprocess import Popen, PIPE
from time import time
import io
import os
from .utils import DEVNULL, memoize, cache


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

    def app_alias(self, fuck):
        return "alias {0}='TF_ALIAS={0} eval $(thefuck $(fc -ln -1))'".format(fuck)

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

    def _script_from_history(self, line):
        """Returns prepared history line.

        Should return a blank line if history line is corrupted or empty.

        """
        return ''

    def get_history(self):
        """Returns list of history entries."""
        history_file_name = self._get_history_file_name()
        if os.path.isfile(history_file_name):
            with io.open(history_file_name, 'r',
                         encoding='utf-8', errors='ignore') as history:
                for line in history:
                    prepared = self._script_from_history(line)\
                                   .strip()
                    if prepared:
                        yield prepared

    def and_(self, *commands):
        return u' && '.join(commands)

    def how_to_configure(self):
        return


class Bash(Generic):
    def app_alias(self, fuck):
        return "TF_ALIAS={0} alias {0}='eval $(thefuck $(fc -ln -1));" \
               " history -r'".format(fuck)

    def _parse_alias(self, alias):
        name, value = alias.replace('alias ', '', 1).split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    @memoize
    @cache('.bashrc', '.bash_profile')
    def get_aliases(self):
        proc = Popen(['bash', '-ic', 'alias'], stdout=PIPE, stderr=DEVNULL)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias and '=' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.bash_history'))

    def _get_history_line(self, command_script):
        return u'{}\n'.format(command_script)

    def _script_from_history(self, line):
        return line

    def how_to_configure(self):
        if os.path.join(os.path.expanduser('~'), '.bashrc'):
            config = '~/.bashrc'
        elif os.path.join(os.path.expanduser('~'), '.bash_profile'):
            config = '~/.bashrc'
        else:
            config = 'bash config'
        return 'eval $(thefuck --alias)', config


class Fish(Generic):

    def _get_overridden_aliases(self):
        overridden_aliases = os.environ.get('TF_OVERRIDDEN_ALIASES', '').strip()
        if overridden_aliases:
            return [alias.strip() for alias in overridden_aliases.split(',')]
        else:
            return ['cd', 'grep', 'ls', 'man', 'open']

    def app_alias(self, fuck):
        return ("set TF_ALIAS {0}\n"
                "function {0} -d 'Correct your previous console command'\n"
                "    set -l exit_code $status\n"
                "    set -l eval_script"
                " (mktemp 2>/dev/null ; or mktemp -t 'thefuck')\n"
                "    set -l fucked_up_command $history[1]\n"
                "    thefuck $fucked_up_command > $eval_script\n"
                "    . $eval_script\n"
                "    /bin/rm $eval_script\n"
                "    if test $exit_code -ne 0\n"
                "        history --delete $fucked_up_command\n"
                "    end\n"
                "end").format(fuck)

    @memoize
    def get_aliases(self):
        overridden = self._get_overridden_aliases()
        proc = Popen(['fish', '-ic', 'functions'], stdout=PIPE, stderr=DEVNULL)
        functions = proc.stdout.read().decode('utf-8').strip().split('\n')
        return {func: func for func in functions if func not in overridden}

    def _expand_aliases(self, command_script):
        aliases = self.get_aliases()
        binary = command_script.split(' ')[0]
        if binary in aliases:
            return u'fish -ic "{}"'.format(command_script.replace('"', r'\"'))
        else:
            return command_script

    def from_shell(self, command_script):
        """Prepares command before running in app."""
        return self._expand_aliases(command_script)

    def _get_history_file_name(self):
        return os.path.expanduser('~/.config/fish/fish_history')

    def _get_history_line(self, command_script):
        return u'- cmd: {}\n   when: {}\n'.format(command_script, int(time()))

    def and_(self, *commands):
        return u'; and '.join(commands)

    def how_to_configure(self):
        return 'eval thefuck --alias', '~/.config/fish/config.fish'


class Zsh(Generic):
    def app_alias(self, fuck):
        return "TF_ALIAS={0}" \
               " alias {0}='eval $(thefuck $(fc -ln -1 | tail -n 1));" \
               " fc -R'".format(fuck)

    def _parse_alias(self, alias):
        name, value = alias.split('=', 1)
        if value[0] == value[-1] == '"' or value[0] == value[-1] == "'":
            value = value[1:-1]
        return name, value

    @memoize
    @cache('.zshrc')
    def get_aliases(self):
        proc = Popen(['zsh', '-ic', 'alias'], stdout=PIPE, stderr=DEVNULL)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias and '=' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.zsh_history'))

    def _get_history_line(self, command_script):
        return u': {}:0;{}\n'.format(int(time()), command_script)

    def _script_from_history(self, line):
        if ';' in line:
            return line.split(';', 1)[1]
        else:
            return ''

    def how_to_configure(self):
        return 'eval $(thefuck --alias)', '~/.zshrc'


class Tcsh(Generic):
    def app_alias(self, fuck):
        return ("alias {0} 'setenv TF_ALIAS {0} && "
                "set fucked_cmd=`history -h 2 | head -n 1` && "
                "eval `thefuck ${{fucked_cmd}}`'").format(fuck)

    def _parse_alias(self, alias):
        name, value = alias.split("\t", 1)
        return name, value

    @memoize
    def get_aliases(self):
        proc = Popen(['tcsh', '-ic', 'alias'], stdout=PIPE, stderr=DEVNULL)
        return dict(
            self._parse_alias(alias)
            for alias in proc.stdout.read().decode('utf-8').split('\n')
            if alias and '\t' in alias)

    def _get_history_file_name(self):
        return os.environ.get("HISTFILE",
                              os.path.expanduser('~/.history'))

    def _get_history_line(self, command_script):
        return u'#+{}\n{}\n'.format(int(time()), command_script)

    def how_to_configure(self):
        return 'eval `thefuck --alias`', '~/.tcshrc'


shells = defaultdict(Generic, {
    'bash': Bash(),
    'fish': Fish(),
    'zsh': Zsh(),
    'csh': Tcsh(),
    'tcsh': Tcsh()})


@memoize
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


def app_alias(alias):
    return _get_shell().app_alias(alias)


def thefuck_alias():
    return os.environ.get('TF_ALIAS', 'fuck')


def put_to_history(command):
    return _get_shell().put_to_history(command)


def and_(*commands):
    return _get_shell().and_(*commands)


def get_aliases():
    return list(_get_shell().get_aliases().keys())


@memoize
def get_history():
    return list(_get_shell().get_history())

def how_to_configure():
    return _get_shell().how_to_configure()
