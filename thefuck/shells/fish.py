from subprocess import Popen, PIPE
from time import time
import os
import sys
import six
from .. import logs
from ..conf import settings
from ..utils import DEVNULL, memoize, cache
from .generic import Generic


class Fish(Generic):
    def _get_overridden_aliases(self):
        overridden = os.environ.get('THEFUCK_OVERRIDDEN_ALIASES',
                                    os.environ.get('TF_OVERRIDDEN_ALIASES', ''))
        default = {'cd', 'grep', 'ls', 'man', 'open'}
        for alias in overridden.split(','):
            default.add(alias.strip())
        return default

    def app_alias(self, fuck):
        if settings.alter_history:
            alter_history = ('    history --delete $fucked_up_command\n'
                             '    history --merge ^ /dev/null\n')
        else:
            alter_history = ''
        # It is VERY important to have the variables declared WITHIN the alias
        return ('function {0} -d "Correct your previous console command"\n'
                '  set -l fucked_up_command $history[1]\n'
                '  env TF_ALIAS={0} PYTHONIOENCODING=utf-8'
                ' thefuck $fucked_up_command | read -l unfucked_command\n'
                '  if [ "$unfucked_command" != "" ]\n'
                '    eval $unfucked_command\n{1}'
                '  end\n'
                'end').format(fuck, alter_history)

    @memoize
    @cache('.config/fish/config.fish', '.config/fish/functions')
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

    def _get_history_file_name(self):
        return os.path.expanduser('~/.config/fish/fish_history')

    def _get_history_line(self, command_script):
        return u'- cmd: {}\n   when: {}\n'.format(command_script, int(time()))

    def _script_from_history(self, line):
        if '- cmd: ' in line:
            return line.split('- cmd: ', 1)[1]
        else:
            return ''

    def and_(self, *commands):
        return u'; and '.join(commands)

    def how_to_configure(self):
        return (r"eval (thefuck --alias | tr '\n' ';')",
                '~/.config/fish/config.fish')

    def put_to_history(self, command):
        try:
            return self._put_to_history(command)
        except IOError:
            logs.exception("Can't update history", sys.exc_info())

    def _put_to_history(self, command_script):
        """Puts command script to shell history."""
        history_file_name = self._get_history_file_name()
        if os.path.isfile(history_file_name):
            with open(history_file_name, 'a') as history:
                entry = self._get_history_line(command_script)
                if six.PY2:
                    history.write(entry.encode('utf-8'))
                else:
                    history.write(entry)
