from thefuck.specific.git import git_support
from thefuck.utils import replace_argument


@git_support
def match(command):
    return ('set-url' in command.script
            and 'fatal: No such remote' in command.output)


def get_new_command(command):
    return replace_argument(command.script, 'set-url', 'add')
