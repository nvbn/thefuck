import re
from thefuck.utils import get_closest, replace_command
from thefuck.specific.brew import brew_available, all_brew_commands

enabled_by_default = brew_available


def match(command):
    is_proper_command = ('brew' in command.script and
                         'Unknown command' in command.output)

    if is_proper_command:
        broken_cmd = re.findall(r'Error: Unknown command: ([a-z]+)',
                                command.output)[0]
        return bool(get_closest(broken_cmd, all_brew_commands()))
    return False


def get_new_command(command):
    broken_cmd = re.findall(r'Error: Unknown command: ([a-z]+)',
                            command.output)[0]
    return replace_command(command, broken_cmd, all_brew_commands())
