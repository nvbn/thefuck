import os

from thefuck.utils import for_app


def _get_actual_file(parts):
    for part in parts[1:]:
        if os.path.isfile(part) or os.path.isdir(part):
            return part


@for_app('grep', 'egrep')
def match(command):
    return ': No such file or directory' in command.output \
        and _get_actual_file(command.script_parts)


def get_new_command(command):
    actual_file = _get_actual_file(command.script_parts)
    parts = command.script_parts[::]
    # Moves file to the end of the script:
    parts.remove(actual_file)
    parts.append(actual_file)
    return ' '.join(parts)
