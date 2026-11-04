import re

from thefuck.utils import for_app


@for_app('man', at_least=1)
def match(command):
    return True


def get_new_command(command):
    section = re.match(r'^\S+\s+(?:-s\s*)?([23])(?=\s)', command.script)
    if section:
        start, end = section.span(1)
        replacement = '2' if section.group(1) == '3' else '3'
        return command.script[:start] + replacement + command.script[end:]

    last_arg = command.script_parts[-1]
    help_command = last_arg + ' --help'

    # If there are no man pages for last_arg, suggest `last_arg --help` instead.
    # Otherwise, suggest `--help` after suggesting other man page sections.
    if command.output.strip() == 'No manual entry for ' + last_arg:
        return [help_command]

    split_cmd2 = command.script_parts
    split_cmd3 = split_cmd2[:]

    split_cmd2.insert(1, ' 2 ')
    split_cmd3.insert(1, ' 3 ')

    return [
        "".join(split_cmd3),
        "".join(split_cmd2),
        help_command,
    ]
