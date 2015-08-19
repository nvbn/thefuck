from thefuck.utils import replace_command
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

    return replace_command(command, old_cmd, suggestions)
