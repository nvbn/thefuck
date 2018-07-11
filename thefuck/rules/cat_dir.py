import os
from thefuck.utils import for_app


@for_app('cat', at_least=1)
def match(command):
    return (
        command.output.startswith('cat: ') and
        os.path.isdir(command.script_parts[1])
    )


def get_new_command(command):
    return command.script.replace('cat', 'ls', 1)
