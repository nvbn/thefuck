from difflib import get_close_matches
from thefuck.utils import get_closest, get_valid_history_without_current


def match(command):
    return len(get_close_matches(command.script,
                                 get_valid_history_without_current(command)))


def get_new_command(command):
    return get_closest(command.script,
                       get_valid_history_without_current(command))


priority = 9999
