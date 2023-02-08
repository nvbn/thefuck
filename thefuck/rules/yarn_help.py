import re

from thefuck.system import open_command
from thefuck.utils import for_app


@for_app('yarn', at_least=2)
def match(command):
    return (command.script_parts[1] == 'help'
            and 'for documentation about this command.' in command.output)


def get_new_command(command):
    url = re.findall(
        r'Visit ([^ ]*) for documentation about this command.',
        command.output)[0]

    return open_command(url)
