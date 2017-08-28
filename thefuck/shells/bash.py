import os
from uuid import uuid4
from ..conf import settings
from ..const import ARGUMENT_PLACEHOLDER, USER_COMMAND_MARK
from ..utils import memoize
from .generic import Generic


class Bash(Generic):
    def app_alias(self, alias_name):
        # It is VERY important to have the variables declared WITHIN the function
        return '''
            function {name} () {{
                TF_PREVIOUS=$(fc -ln -1);
                TF_PYTHONIOENCODING=$PYTHONIOENCODING;
                export TF_ALIAS={name};
                export TF_SHELL_ALIASES=$(alias);
                export PYTHONIOENCODING=utf-8;
                TF_CMD=$(
                    thefuck $TF_PREVIOUS {argument_placeholder} $@
                ) && eval $TF_CMD;
                export PYTHONIOENCODING=$TF_PYTHONIOENCODING;
                {alter_history}
            }}
        '''.format(
            name=alias_name,
            argument_placeholder=ARGUMENT_PLACEHOLDER,
            alter_history=('history -s $TF_CMD;'
                           if settings.alter_history else ''))

    def instant_mode_alias(self, alias_name):
        if os.environ.get('THEFUCK_INSTANT_MODE', '').lower() == 'true':
            return '''
                export PS1="{user_command_mark}$PS1";
                {app_alias}
            '''.format(user_command_mark=USER_COMMAND_MARK,
                       app_alias=self.app_alias(alias_name))
        else:
            return '''
                export THEFUCK_INSTANT_MODE=True;
                export THEFUCK_OUTPUT_LOG={log};
                script -feq {log};
                exit
            '''.format(log='/tmp/thefuck-script-log-{}'.format(uuid4().hex))

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
            config = '~/.bash_profile'
        else:
            config = 'bash config'

        return self._create_shell_configuration(
            content=u'eval $(thefuck --alias)',
            path=config,
            reload=u'source {}'.format(config))
