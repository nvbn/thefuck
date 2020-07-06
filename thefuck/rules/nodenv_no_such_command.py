import re
from thefuck.utils import cache, for_app, replace_argument, replace_command, which
from thefuck.specific.devenv import env_available, COMMON_TYPOS
from subprocess import PIPE, Popen

enabled_by_default = env_available


@for_app('nodenv')
def match(command):
    return 'nodenv: no such command' in command.output


def get_commands():
    proc = Popen(['nodenv', 'commands'], stdout=PIPE)
    return [line.decode('utf-8').strip() for line in proc.stdout.readlines()]


if which('nodenv'):
    get_commands = cache(which('nodenv'))(get_commands)


@for_app('nodenv')
def get_new_command(command):
    broken = re.findall(r"nodenv: no such command `([^']*)'", command.output)[0]
    matched = [replace_argument(command.script, broken, common_typo)
               for common_typo in COMMON_TYPOS.get(broken, [])]
    matched.extend(replace_command(command, broken, get_commands()))
    return matched
