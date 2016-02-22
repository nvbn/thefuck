from subprocess import Popen, PIPE
from time import time
import os
from ..conf import settings
from ..utils import DEVNULL, memoize, cache
from .generic import Generic


class Zsh(Generic):
    def app_alias(self, fuck):
        alias = "alias {0}='TF_ALIAS={0} PYTHONIOENCODING=utf-8" \
                " TF_CMD=$(thefuck $(fc -ln -1 | tail -n 1)) &&" \
                " eval $TF_CMD".format(fuck)

        if settings.alter_history:
            return alias + " && print -s $TF_CMD'"
        else:
            return alias + "'"

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
