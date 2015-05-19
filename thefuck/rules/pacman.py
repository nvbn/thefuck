import subprocess
from thefuck.utils import DEVNULL, which
from thefuck import shells


def __get_pkgfile(command):
    try:
        return subprocess.check_output(
            ['pkgfile', '-b', '-v', command.script.split(" ")[0]],
            universal_newlines=True, stderr=DEVNULL
        ).split()
    except subprocess.CalledProcessError:
        return None


def match(command, settings):
    return 'not found' in command.stderr and __get_pkgfile(command)


def get_new_command(command, settings):
    package = __get_pkgfile(command)[0]

    formatme = shells.and_('{} -S {}', '{}')
    return formatme.format(pacman, package, command.script)


if not which('pkgfile'):
    enabled_by_default = False
elif which('yaourt'):
    pacman = 'yaourt'
elif which('pacman'):
    pacman = 'sudo pacman'
else:
    enabled_by_default = False
