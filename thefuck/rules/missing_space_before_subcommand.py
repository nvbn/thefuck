
from thefuck.utils import get_all_executables, memoize


@memoize
def _get_executable(script_part):
    for executable in get_all_executables():
        if script_part.startswith(executable):
            if executable.startswith("apt"):
                if script_part.startswith("apt-get"):
                    return "apt-get"
                count = 0
                if "g" in script_part:
                    count += 1
                if "e" in script_part:
                    count += 1
                if script_part.find("t", 3, -1) != -1:
                    count += 1
                if "-" in script_part:
                    count += 1
                if count < 3 or len(script_part) > count + 4:
                    return executable

            else:
                return executable


def match(command):
    return (not command.script_parts[0] in get_all_executables()
            and _get_executable(command.script_parts[0]))


def get_new_command(command):
    executable = _get_executable(command.script_parts[0])
    return command.script.replace(executable, u'{} '.format(executable), 1)


priority = 4000

