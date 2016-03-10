from subprocess import Popen, PIPE
from time import time
import os
from ..utils import DEVNULL, memoize, cache
from .generic import Generic


class Fish(Generic):
    def _get_overridden_aliases(self):
        overridden_aliases = os.environ.get('TF_OVERRIDDEN_ALIASES', '').strip()
        if overridden_aliases:
            return [alias.strip() for alias in overridden_aliases.split(',')]
        else:
            return ['cd', 'grep', 'ls', 'man', 'open']

    def app_alias(self, fuck):
        # It is VERY important to have the variables declared WITHIN the alias
        return ('function {0} -d "Correct your previous console command"\n'
                '  set -l fucked_up_command $history[1]\n'
                '  env TF_ALIAS={0} PYTHONIOENCODING=utf-8'
                ' thefuck $fucked_up_command | read -l unfucked_command\n'
                '  if [ "$unfucked_command" != "" ]\n'
                '    eval $unfucked_command\n'
                '    history --delete $fucked_up_command\n'
                '    history --merge ^ /dev/null\n'
                '  end\n'
                'end').format(fuck)

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

    def from_shell(self, command_script):
        """Prepares command before running in app."""
        return self._expand_aliases(command_script)

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
