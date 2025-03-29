from thefuck.utils import get_all_executables
from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command):
    first_part = command.script_parts[0]
    if "-" not in first_part or first_part in get_all_executables():
        return False
    cmd, _ = first_part.split("-", 1)
    return cmd in get_all_executables()


@sudo_support
def get_new_command(command):
    return command.script.replace("-", " ", 1)


priority = 4500
requires_output = False
