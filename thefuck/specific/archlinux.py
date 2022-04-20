""" This file provide some utility functions for Arch Linux specific rules."""
import subprocess
from .. import utils


@utils.memoize
def get_pkgfile(command):
    """ Gets the packages that provide the given command using `pkgfile`.

    If the command is of the form `sudo foo`, searches for the `foo` command
    instead.
    """
    try:
        command = command.strip()

        if command.startswith('sudo '):
            command = command[5:]

        command = command.split(" ")[0]

        packages = subprocess.check_output(
            ['pkgfile', '-b', '-v', command],
            universal_newlines=True, stderr=utils.DEVNULL
        ).splitlines()

        return [package.split()[0] for package in packages]
    except subprocess.CalledProcessError as err:
        if err.returncode == 1 and err.output == "":
            return []
        else:
            raise err


def archlinux_env():
    if utils.which('yay'):
        pacman = 'yay'
    elif utils.which('pikaur'):
        pacman = 'pikaur'
    elif utils.which('yaourt'):
        pacman = 'yaourt'
    elif utils.which('pacman'):
        pacman = 'sudo pacman'
    else:
        return False, None

    enabled_by_default = utils.which('pkgfile')

    return enabled_by_default, pacman
