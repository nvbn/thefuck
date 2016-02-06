from thefuck.specific.apt import apt_available
from thefuck.utils import memoize
from thefuck.shells import shell

try:
    import CommandNotFound
    enabled_by_default = apt_available
except ImportError:
    enabled_by_default = False


@memoize
def get_package(command):
    try:
        c = CommandNotFound.CommandNotFound()
        cmd = command.split(' ')
        pkgs = c.getPackages(cmd[0] if cmd[0] != 'sudo' else cmd[1])
        name, _ = pkgs[0]
        return name
    except IndexError:
        # IndexError is thrown when no matching package is found
        return None


def match(command):
    return 'not found' in command.stderr and get_package(command.script)


def get_new_command(command):
    name = get_package(command.script)
    formatme = shell.and_('sudo apt-get install {}', '{}')
    return formatme.format(name, command.script)
