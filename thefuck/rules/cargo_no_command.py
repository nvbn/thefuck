import re
from thefuck.utils import replace_argument


def match(command, settings):
    return ('cargo' in command.script
            and 'No such subcommand' in command.stderr
            and 'Did you mean' in command.stderr)


def get_new_command(command, settings):
    broken = command.script.split()[1]
    fix = re.findall(r'Did you mean `([^`]*)`', command.stderr)[0]

    return replace_argument(command.script, broken, fix)
