import re
from thefuck.specific.git import git_support

error_pattern = "fatal: bad flag '(.*?)' used after filename"


@git_support
def match(command):
    return re.search(error_pattern, command.stderr)


@git_support
def get_new_command(command):
    command_parts = command.script_parts[:]

    # find the bad flag
    bad_flag = re.search(error_pattern, command.stderr).group(1)
    bad_flag_index = command_parts.index(bad_flag)

    # find the filename
    for index in reversed(range(bad_flag_index)):
        if command_parts[index][0] != '-':
            filename_index = index
            break

    # swap them
    command_parts[bad_flag_index], command_parts[filename_index] = \
    command_parts[filename_index], command_parts[bad_flag_index]  # noqa: E122

    return u' '.join(command_parts)
