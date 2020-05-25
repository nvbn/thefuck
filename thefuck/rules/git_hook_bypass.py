from thefuck.utils import replace_argument
from thefuck.specific.git import git_support

hooked_commands = ["am", "commit", "push"]


@git_support
def match(command):
    has_hooked_command = any(
        hooked_command in command.script_parts for hooked_command in hooked_commands
    )
    return (
        has_hooked_command
        and "hook failed (add --no-verify to bypass)" in command.output
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
