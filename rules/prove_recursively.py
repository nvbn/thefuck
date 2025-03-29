import os
from thefuck.utils import for_app


def _is_recursive(part):
    if part == '--recurse':
        return True
    elif not part.startswith('--') and part.startswith('-') and 'r' in part:
        return True


def _isdir(part):
    return not part.startswith('-') and os.path.isdir(part)


@for_app('prove')
def match(command):
    return (
        'NOTESTS' in command.output
        and not any(_is_recursive(part) for part in command.script_parts[1:])
        and any(_isdir(part) for part in command.script_parts[1:]))


def get_new_command(command):
    parts = command.script_parts[:]
    parts.insert(1, '-r')
    return u' '.join(parts)
