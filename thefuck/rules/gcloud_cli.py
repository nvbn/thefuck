import re 

from thefuck.utils import for_app, replace_argument

INVALID_CHOICE = "(?<=Invalid choice: ')(.*)(?='.)"
OPTIONS = "t\\:\\n\\s\\s(.*)"


@for_app('gcloud')
def match(command):
    return "ERROR:" in command.output and "Maybe you meant:" in command.output


def get_new_command(command):
    mistake = re.search(INVALID_CHOICE, command.output).group(0)
    options = re.findall(OPTIONS, command.output, flags=re.MULTILINE)
    return options
#[replace_argument(command.script, mistake, o) for o in options]
