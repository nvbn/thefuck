from difflib import get_close_matches
from thefuck.utils import sudo_support, get_all_executables, get_closest


@sudo_support
def match(command, settings):
    return 'not found' in command.stderr and \
           bool(get_close_matches(command.script.split(' ')[0],
                                  get_all_executables()))


@sudo_support
def get_new_command(command, settings):
    old_command = command.script.split(' ')[0]
    new_command = get_closest(old_command, get_all_executables())
    return ' '.join([new_command] + command.script.split(' ')[1:])


priority = 3000
