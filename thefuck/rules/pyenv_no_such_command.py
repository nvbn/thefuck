import re
from thefuck.utils import cache, for_app, replace_argument, replace_command, which
from thefuck.specific.devenv import env_available, COMMON_TYPOS, get_commands

enabled_by_default = env_available


@for_app('pyenv')
def match(command):
    return 'pyenv: no such command' in command.output


if which('pyenv'):
    get_commands = cache(which('pyenv'))(get_commands)


@for_app('pyenv')
def get_new_command(command):
    broken = re.findall(r"pyenv: no such command `([^']*)'", command.output)[0]
    matched = [replace_argument(command.script, broken, common_typo)
               for common_typo in COMMON_TYPOS.get(broken, [])]
    matched.extend(replace_command(command, broken, get_commands()))
    return matched
