import re
from thefuck.utils import for_app

MISTAKE = r"(?<=Terraform has no command named \")(.*)(?=\"\.)"
FIX = r"(?<=Did you mean \")(.*)(?=\"\?)"


@for_app('terraform')
def match(command):
    return ('Terraform has no command named' in command.output and 'Did you mean' in command.output)


def get_new_command(command):
    mistake = re.search(MISTAKE, command.output).group(0)
    fix = re.search(FIX, command.output).group(0)
    return command.script.replace(mistake, fix)
