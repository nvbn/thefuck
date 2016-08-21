from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('push' in command.script
            and 'set-upstream' in command.stderr)


@git_support
def get_new_command(command):
    push_upstream = command.stderr.split('\n')[-3].strip().partition('git ')[2]
    return replace_argument(command.script, 'push', push_upstream)
