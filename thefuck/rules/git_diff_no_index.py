from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    files = [arg for arg in command.script_parts[2:]
             if not arg.startswith('-')]
    return ('diff' in command.script
            and '--no-index' not in command.script
            and not command.stdout
            and len(files) == 2)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'diff', 'diff --no-index')
