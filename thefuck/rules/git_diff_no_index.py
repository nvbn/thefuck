from six.moves import filterfalse
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    args = command.script_parts[2:]
    files = list(filterfalse(is_option, args))
    return ('diff' in command.script and
            '--no-index' not in command.script and
            len(command.stdout) is 0 and
            len(files) is 2)

def is_option(script_part):
    return script_part.startswith('-')

@git_support
def get_new_command(command):
    return replace_argument(command.script, 'diff', 'diff --no-index')
