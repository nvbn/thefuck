from thefuck.specific.git import git_support
from thefuck.utils import replace_argument


@git_support
def match(command):
    return ('fatal: Not a git repository' in command.output
            and "Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)." in command.output)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'pull', 'clone')
