from difflib import get_close_matches
from thefuck.shells import get_history, thefuck_alias
from thefuck.utils import get_closest, memoize
from thefuck.rules.no_command import get_all_callables


def _not_corrected(history, tf_alias):
    """Returns all lines from history except that comes before `fuck`."""
    previous = None
    for line in history:
        if previous is not None and line != tf_alias:
            yield previous
        previous = line
    yield history[-1]


@memoize
def _history_of_exists_without_current(command):
    history = get_history()
    tf_alias = thefuck_alias()
    callables = get_all_callables()
    return [line for line in _not_corrected(history, tf_alias)
            if not line.startswith(tf_alias) and not line == command.script
            and line.split(' ')[0] in callables]

def match(command, settings):
    return len(get_close_matches(command.script,
                                 _history_of_exists_without_current(command)))


def get_new_command(command, settings):
    return get_closest(command.script,
                       _history_of_exists_without_current(command))


priority = 9999
