from thefuck import utils
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return (command.script.split()[1] == 'stash'
            and 'usage:' in command.stderr)

# git's output here is too complicated to be parsed (see the test file)
stash_commands = (
    'apply',
    'branch',
    'clear',
    'drop',
    'list',
    'pop',
    'save',
    'show')


@git_support
def get_new_command(command):
    stash_cmd = command.script.split()[2]
    fixed = utils.get_closest(stash_cmd, stash_commands, fallback_to_first=False)

    if fixed is not None:
        return replace_argument(command.script, stash_cmd, fixed)
    else:
        cmd = command.script.split()
        cmd.insert(2, 'save')
        return ' '.join(cmd)
