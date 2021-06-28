import re


SUGGESTION_REGEX = r"To resolve this issue, run:\s+(.*?)\n"


def match(command):
    return ("Migrations are pending. To resolve this issue, run:" in command.output)


def get_new_command(command):
    return re.search(SUGGESTION_REGEX, command.output).group(1)
