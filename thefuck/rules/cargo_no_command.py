import re
from thefuck.utils import replace_argument, for_app


@for_app('cargo', at_least=1)
def match(command):
    return (
        'no such subcommand' in command.output.lower()
        and 'Did you mean' in command.output
    )


def get_new_command(command):
    broken = command.script_parts[1]
    fix = re.findall(r'Did you mean `([^`]*)`', command.output)[0]

    return replace_argument(command.script, broken, fix)
