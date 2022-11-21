import re

from thefuck.utils import for_app, get_all_matched_commands, replace_argument


@for_app('kedro')
def match(command):
    return 'No such command ' in command.output and 'Did you mean ' in command.output


def _get_single_matched_command(stderr):
    """Matches one suggestion found on the same line as 'Did you mean '.

    If Kedro only finds one match, it prints it on the same line instead
    of on a new line. This won't work with ``get_all_matched_commands``.

    """
    return re.findall(r'Did you mean this\?\s*(\w+)', stderr)


def get_new_command(command):
    broken_cmd = re.findall(r"No such command '([^']*)'.", command.output)[0]
    new_cmds = (_get_single_matched_command(command.output)
                or get_all_matched_commands(command.output))

    # Kedro already uses `difflib.get_close_matches` when suggesting CLI
    # commands, so we don't want `replace_command` to do so differently.
    return [replace_argument(command.script, broken_cmd, new_cmd)
            for new_cmd in new_cmds]
