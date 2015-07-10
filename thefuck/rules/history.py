from difflib import get_close_matches
from thefuck.shells import get_history
from thefuck.utils import get_closest, memoize
from thefuck.rules.no_command import get_all_callables


@memoize
def _history_of_exists_without_current(command):
    callables = get_all_callables()
    return [line for line in get_history()
            if line != command.script
            and line.split(' ')[0] in callables]


def match(command, settings):
    return len(get_close_matches(command.script,
                                 _history_of_exists_without_current(command)))


def get_new_command(command, settings):
    return get_closest(command.script,
                       _history_of_exists_without_current(command))

priority = 9999
