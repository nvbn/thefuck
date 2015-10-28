from difflib import get_close_matches
from thefuck.utils import get_all_executables
from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command):
    return (command.script_parts
            and 'not found' in command.stderr
            and bool(get_close_matches(command.script_parts[0],
                                       get_all_executables())))


@sudo_support
def get_new_command(command):
    old_command = command.script_parts[0]
    new_cmds = get_close_matches(old_command, get_all_executables(), cutoff=0.1)
    return [' '.join([new_command] + command.script_parts[1:])
            for new_command in new_cmds]


priority = 3000
