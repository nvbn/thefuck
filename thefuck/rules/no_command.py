from difflib import get_close_matches
import os
from pathlib import Path
from thefuck.utils import sudo_support
from thefuck.shells import get_aliases


def _safe(fn, fallback):
    try:
        return fn()
    except OSError:
        return fallback


def _get_all_callables():
    return [exe.name
            for path in os.environ.get('PATH', '').split(':')
            for exe in _safe(lambda: list(Path(path).iterdir()), [])
            if not _safe(exe.is_dir, True)] + get_aliases()


@sudo_support
def match(command, settings):
    return 'not found' in command.stderr and \
           bool(get_close_matches(command.script.split(' ')[0],
                                  _get_all_callables()))


@sudo_support
def get_new_command(command, settings):
    old_command = command.script.split(' ')[0]
    new_command = get_close_matches(old_command,
                                    _get_all_callables())[0]
    return ' '.join([new_command] + command.script.split(' ')[1:])


priority = 3000
