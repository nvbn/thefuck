from thefuck import utils
from thefuck.utils import replace_argument


@utils.git_support
def match(command, settings):
    return ('diff' in command.script and
            '--staged' not in command.script)


@utils.git_support
def get_new_command(command, settings):
    return replace_argument(command.script, 'diff', 'diff --staged')
