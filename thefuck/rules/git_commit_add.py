from thefuck.utils import replace_argument
from thefuck.specific.git import git_support

priority = 900  # Lower first, default is 1000


@git_support
def match(command):
    return ('commit' in command.script_parts
            and 'no changes added to commit' in command.output)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'commit', 'commit -a')
