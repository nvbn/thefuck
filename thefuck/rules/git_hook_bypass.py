from thefuck.utils import replace_argument
from thefuck.specific.git import git_support

hooked_commands = ("am", "commit", "push")


@git_support
def match(command):
    return any(
        hooked_command in command.script_parts for hooked_command in hooked_commands
    )


@git_support
def get_new_command(command):
    hooked_command = next(
        hooked_command
        for hooked_command in hooked_commands
        if hooked_command in command.script_parts
    )
    return replace_argument(
        command.script, hooked_command, hooked_command + " --no-verify"
    )


priority = 900
requires_output = False
