from thefuck.utils import get_closest, replace_argument
import re


def match(command, settings):
    return ('tmux' in command.script
            and 'ambiguous command:' in command.stderr
            and 'could be:' in command.stderr)


def get_new_command(command, settings):
    cmd = re.match(r"ambiguous command: (.*), could be: (.*)",
                   command.stderr)

    old_cmd = cmd.group(1)
    suggestions = [cmd.strip() for cmd in cmd.group(2).split(',')]

    new_cmd = get_closest(old_cmd, suggestions)

    return replace_argument(command.script, old_cmd, new_cmd)
