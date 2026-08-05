from os.path import splitext

from thefuck.utils import get_all_executables, get_close_matches, \
    get_valid_history_without_current, get_closest, which
from thefuck.specific.sudo import sudo_support



def _normalize_executable(executable):
    """
    Normalize executable names.

    Windows executable files contain extensions:
    git.exe -> git
    python.exe -> python

    The shell hides these extensions, so match against the command name.
    """
    return splitext(executable)[0]


def _get_normalized_executables():
    return list(dict.fromkeys(
        _normalize_executable(exe)
        for exe in get_all_executables()
    ))


def _get_executable_matches(command):
    matches = get_close_matches(
        command,
        _get_normalized_executables()
    )

    # Prefer shorter commands when matches are similar.
    # Example:
    # gitr -> git before gitk
    return sorted(matches, key=len)


@sudo_support
def match(command):
    return (not which(command.script_parts[0])
            and ('not found' in command.output
                 or 'is not recognized as' in command.output)
            and bool(_get_executable_matches(command.script_parts[0])))


def _get_used_executables(command):
    for script in get_valid_history_without_current(command):
        yield script.split(' ')[0]


@sudo_support
def get_new_command(command):
    old_command = command.script_parts[0]

    # One from history:
    already_used = get_closest(
        old_command,
        _get_used_executables(command),
        fallback_to_first=False
    )

    if already_used:
        new_cmds = [already_used]
    else:
        new_cmds = []

    # Other from all executables:
    new_cmds += [
        cmd for cmd in _get_executable_matches(old_command)
        if cmd not in new_cmds
    ]

    return [
        command.script.replace(old_command, cmd, 1)
        for cmd in new_cmds
    ]


priority = 3000