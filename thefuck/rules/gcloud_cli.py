import re

from thefuck.utils import for_app

INVALID_CHOICE = "(?<=Invalid choice: ')(.*)(?='.)"
OPTIONS = "t\\:\\n\\s\\s(.*)"


@for_app('gcloud')
def match(command):
    return "ERROR:" in command.output and "Maybe you meant:" in command.output


def get_new_command(command):
    options = re.findall(OPTIONS, command.output, flags=re.MULTILINE)
    return options
