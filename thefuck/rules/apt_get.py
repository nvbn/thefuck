from thefuck.specific.apt import apt_available
from thefuck.utils import memoize, which
from thefuck.shells import shell

try:
    from CommandNotFound import CommandNotFound

    command_not_found = CommandNotFound()
    enabled_by_default = apt_available
except ImportError:
    enabled_by_default = False


def _get_executable(command):
    if command.script_parts[0] == 'sudo':
        return command.script_parts[1]
    else:
        return command.script_parts[0]


@memoize
def get_package(executable):
    try:
        packages = command_not_found.getPackages(executable)
        return packages[0][0]
    except IndexError:
        # IndexError is thrown when no matching package is found
        return None


def match(command):
    if 'not found' in command.stderr or 'not installed' in command.stderr:
        executable = _get_executable(command)
        return not which(executable) and get_package(executable)
    else:
        return False


def get_new_command(command):
    executable = _get_executable(command)
    name = get_package(executable)
    formatme = shell.and_('sudo apt-get install {}', '{}')
    return formatme.format(name, command.script)
