from time import time
import os
import sys
import six
from .. import logs
from ..conf import settings
from .generic import Generic
from ..utils import memoize


class Fish(Generic):
    def _get_overridden_aliases(self):
        overridden = os.environ.get('THEFUCK_OVERRIDDEN_ALIASES',
                                    os.environ.get('TF_OVERRIDDEN_ALIASES', ''))
        default = {'cd', 'grep', 'ls', 'man', 'open'}
        for alias in overridden.split(','):
            default.add(alias.strip())
        return default

    def app_alias(self, alias_name):
        if settings.alter_history:
            alter_history = ('    builtin history delete --exact'
                             ' --case-sensitive -- $fucked_up_command\n'
                             '    builtin history merge ^ /dev/null\n')
        else:
            alter_history = ''
        # It is VERY important to have the variables declared WITHIN the alias
        return ('function {0} -d "Correct your previous console command"\n'
                '  set -l fucked_up_command $history[1]\n'
                '  env TF_SHELL=fish TF_SHELL_ALIASES=(string join \| (alias))'
                ' TF_SHELL_FUNCTIONS=(string join \| (functions))'
                ' TF_ALIAS={0} PYTHONIOENCODING=utf-8'
                ' thefuck $fucked_up_command | read -l unfucked_command\n'
                '  if [ "$unfucked_command" != "" ]\n'
                '    eval $unfucked_command\n{1}'
                '  end\n'
                'end').format(alias_name, alter_history)

    def _get_functions(self, overridden):
        functions = os.environ.get('TF_SHELL_FUNCTIONS', '').split('|')
        logs.debug(functions)
        return {func: func for func in functions if func not in overridden and func != ''}

    def _get_aliases(self, overridden):
        aliases = {}
        alias_out = os.environ.get('TF_SHELL_ALIASES', '').split('|')
        logs.debug(alias_out)
        for alias in [alias for alias in alias_out if alias != '']:
            name, value = alias.replace('alias ', '', 1).split(' ', 1)
            if name not in overridden:
                aliases[name] = value
        return aliases

    @memoize
    def get_aliases(self):
        overridden = self._get_overridden_aliases()
        functions = self._get_functions(overridden)
        raw_aliases = self._get_aliases(overridden)
        functions.update(raw_aliases)
        return functions

    def _expand_aliases(self, command_script):
        aliases = self.get_aliases()
        binary = command_script.split(' ')[0]
        if binary in aliases and aliases[binary] != binary:
            return command_script.replace(binary, aliases[binary], 1)
        elif binary in aliases:
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

    def or_(self, *commands):
        return u'; or '.join(commands)

    def how_to_configure(self):
        return self._create_shell_configuration(
            content=u"thefuck --alias | source",
            path='~/.config/fish/config.fish',
            reload='fish')

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
