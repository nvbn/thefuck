import re

from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, replace_argument


@sudo_support
@for_app('pip', 'pip2', 'pip3')
def match(command):
    return ('pip' in command.script and
            'unknown command' in command.output and
            'maybe you meant' in command.output)


def get_new_command(command):
    broken_cmd = re.findall(r'ERROR: unknown command "([^"]+)"',
                            command.output)[0]
    new_cmd = re.findall(r'maybe you meant "([^"]+)"', command.output)[0]

    return replace_argument(command.script, broken_cmd, new_cmd)
