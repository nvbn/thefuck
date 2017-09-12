from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('error: did you mean `' in command.output
            and '` (with two dashes ?)' in command.output)


@git_support
def get_new_command(command):
    to = command.output.split('`')[1]
    return replace_argument(command.script, to[1:], to)
