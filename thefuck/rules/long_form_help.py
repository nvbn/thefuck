from thefuck.utils import replace_argument
import re

# regex to match a suggested help command from the tool output
helpRegex = r"(?:Run|Try) '([^']+)'(?: or '[^']+')? for (?:details|more information)."


def match(command):
    if re.search(helpRegex, command.output, re.I) is not None:
        return True

    if '--help' in command.output:
        return True

    return False


def get_new_command(command):
    if re.search(helpRegex, command.output) is not None:
        matchObj = re.search(helpRegex, command.output, re.I)
        return matchObj.group(1)

    return replace_argument(command.script, '-h', '--help')


enabled_by_default = True
priority = 5000
