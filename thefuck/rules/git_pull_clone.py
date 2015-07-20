import re
from thefuck import utils, shells


@utils.git_support
def match(command, settings):
    return ('git pull' in command.script
            and 'fatal: Not a git repository' in command.stderr
            and "Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)." in command.stderr)


@utils.git_support
def get_new_command(command, settings):
    return command.script.replace(' pull ', ' clone ')
