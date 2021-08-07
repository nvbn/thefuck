from thefuck.utils import get_all_executables
from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command):
    if (
        "-" not in command.script_parts[0]
        or command.script_parts[0] in get_all_executables()
    ):
        return False

    cmd, _ = command.script_parts[0].split("-", 1)
    return cmd in get_all_executables()


@sudo_support
def get_new_command(command):
    return command.script.replace("-", " ", 1)


priority = 2900
requires_output = False
