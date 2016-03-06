from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('set-url' in command.script and 'fatal: No such remote' in command.stderr)


def get_new_command(command):
    return replace_argument(command.script, 'set-url', 'add')


enabled_by_default = True
