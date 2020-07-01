import re
from thefuck.utils import for_app, replace_argument, replace_command
from thefuck.specific.devenv import env_available, COMMON_TYPOS, get_commands

enabled_by_default = env_available


@for_app('goenv')
def match(command):
    return 'goenv: no such command' in command.output


@for_app('goenv')
def get_new_command(command):
    broken = re.findall(r"goenv: no such command '([^']*)'", command.output)[0]
    matched = [replace_argument(command.script, broken, common_typo)
               for common_typo in COMMON_TYPOS.get(broken, [])]
    matched.extend(replace_command(command, broken, get_commands(command)))
    return matched
