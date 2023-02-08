from thefuck.specific.git import git_support
from thefuck.utils import replace_argument


@git_support
def match(command):
    return ('add' in command.script_parts
            and 'Use -f if you really want to add them.' in command.output)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'add', 'add --force')
