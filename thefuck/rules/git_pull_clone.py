from thefuck import utils
from thefuck.utils import replace_argument


@utils.git_support
def match(command, settings):
    return ('fatal: Not a git repository' in command.stderr
            and "Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)." in command.stderr)


@utils.git_support
def get_new_command(command, settings):
    return replace_argument(command.script, 'pull', 'clone')
