from thefuck.specific.git import git_support
from thefuck.utils import replace_argument


@git_support
def match(command):
    return ('diff' in command.script and
            '--staged' not in command.script)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'diff', 'diff --staged')
