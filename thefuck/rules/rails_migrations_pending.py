import re
from thefuck.shells import shell


SUGGESTION_REGEX = r"To resolve this issue, run:\s+(.*?)\n"


def match(command):
    return "Migrations are pending. To resolve this issue, run:" in command.output


def get_new_command(command):
    migration_script = re.search(SUGGESTION_REGEX, command.output).group(1)
    return shell.and_(migration_script, command.script)
