import re
from subprocess import PIPE, Popen

from thefuck.utils import (cache, for_app, replace_argument, replace_command,
                           which)

COMMON_TYPOS = {
    'list': ['versions', 'install --list'],
    'remove': ['uninstall'],
}


@for_app('env')
def match(command):
    return ('env' in command.script and
            'command not found' in command.output)


def get_env_commands():
    proc_env = Popen(['env', 'commands'], stdout=PIPE)
    return [line.decode('utf-8').strip() for line in proc_env.stdout.readlines()]


if which('env'):
    get_env_commands = cache(which('env'))(get_env_commands)


@for_app('env')
def get_new_command(command):
    broken = re.findall(r"command not found `([^']*)'", command.output)[0]
    matched = [replace_argument(command.script, broken, common_typo)
               for common_typo in COMMON_TYPOS.get(broken, [])]
    matched.extend(replace_command(command, broken, get_env_commands()))     
    return matched
