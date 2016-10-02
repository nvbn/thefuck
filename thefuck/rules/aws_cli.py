import re

from thefuck.utils import for_app, replace_argument

INVALID_CHOICE = "(?<=Invalid choice: ')(.*)(?=', maybe you meant:)"
OPTIONS = "^\s*\*\s(.*)"


@for_app('aws')
def match(command):
    return "usage:" in command.stderr and "maybe you meant:" in command.stderr


def get_new_command(command):
    mistake = re.search(INVALID_CHOICE, command.stderr).group(0)
    options = re.findall(OPTIONS, command.stderr, flags=re.MULTILINE)
    return [replace_argument(command.script, mistake, o) for o in options]
