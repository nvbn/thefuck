import six
import subprocess

# FileNotFoundError is only available since Python 3.3
if six.PY2:
    FileNotFoundError = OSError


def __command_available(command):
    try:
        # subprocess.DEVNULL is only available since Python 3.3
        if six.PY2:
            import os
            subprocess.DEVNULL = open(os.devnull, 'w')
        subprocess.check_output([command], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        # command exists but is not happy to be called without any argument
        return True
    except FileNotFoundError:
        return False
    finally:
        # The open file has to be closed
        if six.PY2:
            subprocess.DEVNULL.close()


def __get_pkgfile(command):
    try:
        # subprocess.DEVNULL is only available since Python 3.3
        if six.PY2:
            import os
            subprocess.DEVNULL = open(os.devnull, 'w')
        return subprocess.check_output(
            ['pkgfile', '-b', '-v', command.script.split(" ")[0]],
            universal_newlines=True, stderr=subprocess.DEVNULL
        ).split()
    except subprocess.CalledProcessError:
        return None
    finally:
        # The open file has to be closed
        if six.PY2:
            subprocess.DEVNULL.close()


def match(command, settings):
    return 'not found' in command.stderr and __get_pkgfile(command)


def get_new_command(command, settings):
    package = __get_pkgfile(command)[0]

    return '{} -S {} && {}'.format(pacman, package, command.script)


if not __command_available('pkgfile'):
    enabled_by_default = False
elif __command_available('yaourt'):
    pacman = 'yaourt'
elif __command_available('pacman'):
    pacman = 'sudo pacman'
else:
    enabled_by_default = False
