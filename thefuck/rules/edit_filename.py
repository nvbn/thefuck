import re
from pathlib import Path

from thefuck.shells import shell

EDITORS = ["vim", "emacs", "nano", "vi", "joe", "neovim", "ne", "mc"]


def _get_fixed_edit_files(script):
    if not re.match("({})".format("|".join(EDITORS)), script):
        return

    parts = shell.split_command(script)
    if len(parts) < 2:
        return

    potential_filepath = Path(parts[-1])
    if potential_filepath.is_file():
        return

    for path in potential_filepath.parent.iterdir():
        if path.stem == potential_filepath.name:
            yield str(path)


def match(command):
    for _ in _get_fixed_edit_files(command.script):
        return True
    return False


def get_new_command(command):
    command_parts = shell.split_command(command.script)
    possible_files = _get_fixed_edit_files(command.script)
    possible_commands = []
    for filepath in possible_files:
        command_parts[-1] = filepath
        possible_commands.append(" ".join(command_parts))
    return possible_commands
