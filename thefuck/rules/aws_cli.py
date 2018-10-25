import re

from thefuck.utils import for_app, replace_argument

INVALID_CHOICE = "(?<=Invalid choice: ')(.*)(?=', maybe you meant:)"
OPTIONS = "^\\s*\\*\\s(.*)"


@for_app('aws')
def match(command):
    return "usage:" in command.output and "maybe you meant:" in command.output


def get_new_command(command):
    mistake = re.search(INVALID_CHOICE, command.output).group(0)
    options = re.findall(OPTIONS, command.output, flags=re.MULTILINE)
    return [replace_argument(command.script, mistake, o) for o in options]
