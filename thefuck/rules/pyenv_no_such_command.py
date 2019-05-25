import re
from subprocess import PIPE, Popen

from thefuck.utils import (cache, for_app, replace_argument, replace_command,
                           which)

COMMON_TYPOS = {
    'list': ['versions', 'install --list'],
    'remove': ['uninstall'],
}


@for_app('pyenv')
def match(command):
    return 'pyenv: no such command' in command.output


def get_pyenv_commands():
    proc = Popen(['pyenv', 'commands'], stdout=PIPE)
    return [line.decode('utf-8').strip() for line in proc.stdout.readlines()]


if which('pyenv'):
    get_pyenv_commands = cache(which('pyenv'))(get_pyenv_commands)


@for_app('pyenv')
def get_new_command(command):
    broken = re.findall(r"pyenv: no such command `([^']*)'", command.output)[0]
    matched = [replace_argument(command.script, broken, common_typo)
               for common_typo in COMMON_TYPOS.get(broken, [])]
    matched.extend(replace_command(command, broken, get_pyenv_commands()))
    return matched
