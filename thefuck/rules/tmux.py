import re
from thefuck.utils import replace_command, for_app


@for_app('tmux')
def match(command):
    return ('ambiguous command:' in command.stderr
            and 'could be:' in command.stderr)


def get_new_command(command):
    cmd = re.match(r"ambiguous command: (.*), could be: (.*)",
                   command.stderr)

    old_cmd = cmd.group(1)
    suggestions = [cmd.strip() for cmd in cmd.group(2).split(',')]

    return replace_command(command, old_cmd, suggestions)
