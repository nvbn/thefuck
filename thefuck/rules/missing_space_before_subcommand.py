
from thefuck.utils import get_all_executables, memoize


@memoize
def _get_executables(script_part):
    executable_list = []
    for executable in get_all_executables():
        if script_part.startswith(executable):
            executable_list.append(executable)
    return executable_list


def match(command):
    return (not command.script_parts[0] in get_all_executables()
            and len(_get_executables(command.script_parts[0])) != 0)


def get_new_command(command):
    executables = _get_executables(command.script_parts[0])
    new_command_scripts = []
    #   return all possible command lines
    for each_exec in executables:
        temp_line = command.script
        new_command_scripts.append(temp_line.replace(
            each_exec, u'{} '.format(each_exec), 1))

    return new_command_scripts


priority = 4000
