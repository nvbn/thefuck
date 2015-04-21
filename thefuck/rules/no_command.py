from difflib import get_close_matches
import os
from pathlib import Path


def _get_all_bins():
    return [exe.name
            for path in os.environ['PATH'].split(':')
            for exe in Path(path).iterdir()
            if exe.is_file()]


def match(command, settings):
    return 'not found' in command.stderr and \
           bool(get_close_matches(command.script.split(' ')[0],
                                  _get_all_bins()))


def get_new_command(command, settings):
    old_command = command.script.split(' ')[0]
    new_command = get_close_matches(old_command,
                                    _get_all_bins())[0]
    return ' '.join([new_command] + command.script.split(' ')[1:])
