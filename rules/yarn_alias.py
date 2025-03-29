import re
from thefuck.utils import replace_argument, for_app


@for_app('yarn', at_least=1)
def match(command):
    return 'Did you mean' in command.output


def get_new_command(command):
    broken = command.script_parts[1]
    fix = re.findall(r'Did you mean [`"](?:yarn )?([^`"]*)[`"]', command.output)[0]

    return replace_argument(command.script, broken, fix)
