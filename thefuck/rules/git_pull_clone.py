from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('fatal: Not a git repository' in command.stderr
            and "Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)." in command.stderr)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'pull', 'clone')
