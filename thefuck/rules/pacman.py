import subprocess
from thefuck.utils import DEVNULL, which
from thefuck import shells
from thefuck.utils import memoize


@memoize
def __get_pkgfile(command):
    try:
        command = command.script

        if command.startswith('sudo'):
            command = command[5:]

        command = command.split(" ")[0]

        packages = subprocess.check_output(
            ['pkgfile', '-b', '-v', command],
            universal_newlines=True, stderr=DEVNULL
        ).splitlines()

        return [package.split()[0] for package in packages]
    except subprocess.CalledProcessError:
        return None


def match(command, settings):
    return 'not found' in command.stderr and __get_pkgfile(command)


def get_new_command(command, settings):
    packages = __get_pkgfile(command)

    formatme = shells.and_('{} -S {}', '{}')
    return [formatme.format(pacman, package, command.script)
            for package in packages]


if not which('pkgfile'):
    enabled_by_default = False
elif which('yaourt'):
    pacman = 'yaourt'
elif which('pacman'):
    pacman = 'sudo pacman'
else:
    enabled_by_default = False
