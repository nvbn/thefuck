import os
from ..conf import settings
from ..utils import memoize
from .generic import Generic


class Bash(Generic):
    def app_alias(self, fuck):
        # It is VERY important to have the variables declared WITHIN the alias
        alias = "alias {0}='TF_CMD=$(TF_ALIAS={0}" \
                " PYTHONIOENCODING=utf-8" \
                " TF_SHELL_ALIASES=$(alias)" \
                " thefuck $(fc -ln -1)) &&" \
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
    def get_aliases(self):
        raw_aliases = os.environ.get('TF_SHELL_ALIASES', '').split('\n')
        return dict(self._parse_alias(alias)
                    for alias in raw_aliases if alias and '=' in alias)

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
