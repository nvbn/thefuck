import re
from thefuck.utils import for_app

MISTAKE = r'(?<=Terraform has no command named ")([^"]+)(?="\.)'
FIX = r'(?<=Did you mean ")([^"]+)(?="\?)'


@for_app('terraform')
def match(command):
    return re.search(MISTAKE, command.output) and re.search(FIX, command.output)


def get_new_command(command):
    mistake = re.search(MISTAKE, command.output).group(0)
    fix = re.search(FIX, command.output).group(0)
    return command.script.replace(mistake, fix)
