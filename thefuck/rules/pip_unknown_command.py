import re
from thefuck.utils import replace_argument, for_app
from thefuck.specific.sudo import sudo_support


@sudo_support
@for_app('pip')
def match(command):
    return ('pip' in command.script and
            'unknown command' in command.stderr and
            'maybe you meant' in command.stderr)


def get_new_command(command):
    broken_cmd = re.findall(r'ERROR: unknown command \"([a-z]+)\"',
                            command.stderr)[0]
    new_cmd = re.findall(r'maybe you meant \"([a-z]+)\"', command.stderr)[0]

    return replace_argument(command.script, broken_cmd, new_cmd)
