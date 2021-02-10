import re
from thefuck.utils import (cache, for_app, replace_argument, replace_command,
                           which)
from subprocess import PIPE, Popen


supported_apps = 'goenv', 'nodenv', 'pyenv', 'rbenv'
enabled_by_default = any(which(a) for a in supported_apps)


COMMON_TYPOS = {
    'list': ['versions', 'install --list'],
    'remove': ['uninstall'],
}


@for_app(*supported_apps, at_least=1)
def match(command):
    return 'env: no such command ' in command.output


def get_app_commands(app):
    proc = Popen([app, 'commands'], stdout=PIPE)
    return [line.decode('utf-8').strip() for line in proc.stdout.readlines()]


def get_new_command(command):
    broken = re.findall(r"env: no such command ['`]([^']*)'", command.output)[0]
    matched = [replace_argument(command.script, broken, common_typo)
               for common_typo in COMMON_TYPOS.get(broken, [])]

    app = command.script_parts[0]
    app_commands = cache(which(app))(get_app_commands)(app)
    matched.extend(replace_command(command, broken, app_commands))
    return matched
