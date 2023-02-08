import re

from thefuck.utils import replace_argument

# regex to match a suggested help command from the tool output
help_regex = r"(?:Run|Try) '([^']+)'(?: or '[^']+')? for (?:details|more information)."


def match(command):
    if re.search(help_regex, command.output, re.I) is not None:
        return True

    if '--help' in command.output:
        return True

    return False


def get_new_command(command):
    if re.search(help_regex, command.output) is not None:
        match_obj = re.search(help_regex, command.output, re.I)
        return match_obj.group(1)

    return replace_argument(command.script, '-h', '--help')


enabled_by_default = True
priority = 5000
