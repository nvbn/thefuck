from subprocess import Popen, PIPE
import os
from ..conf import settings
from ..utils import DEVNULL, memoize, cache
from .generic import Generic


class Bash(Generic):
    def app_alias(self, fuck):
        alias = "TF_ALIAS={0}" \
                " alias {0}='PYTHONIOENCODING=utf-8" \
                " TF_CMD=$(thefuck $(fc -ln -1)) && " \
                " eval $TF_CMD".format(fuck)

        if settings.alter_history:
            return alias + " && history -s $TF_CMD'"
        else:
            return alias + "'"

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

    def how_to_configure(self):
        if os.path.join(os.path.expanduser('~'), '.bashrc'):
            config = '~/.bashrc'
        elif os.path.join(os.path.expanduser('~'), '.bash_profile'):
            config = '~/.bashrc'
        else:
            config = 'bash config'
        return 'eval $(thefuck --alias)', config
