from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('tag' in command.script_parts
            and 'already exists' in command.stderr)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'tag', 'tag --force')
