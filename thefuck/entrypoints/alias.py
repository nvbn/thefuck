import subprocess
import urllib.request

import os
import sys
import six
import psutil
from psutil import ZombieProcess

from ..conf import settings
from ..const import SHELL_LOGGER_SOCKET_ENV_VAR, SHELL_LOGGER_SOCKET_PATH, SHELL_LOGGER_BINARY_FILENAME
from ..logs import warn, debug
from ..shells import shell
from ..utils import which


def _get_alias(known_args):
    if six.PY2:
        warn("The Fuck will drop Python 2 support soon, more details "
             "https://github.com/nvbn/thefuck/issues/685")

    alias = shell.app_alias(known_args.alias)

    if known_args.enable_experimental_instant_mode:
        if six.PY2:
            warn("Instant mode requires Python 3")
        elif not which('script'):
            warn("Instant mode requires `script` app")
        else:
            return shell.instant_mode_alias(known_args.alias)

    return alias


def print_alias(known_args):
    print(_get_alias(known_args))


def print_experimental_shell_history(known_args):
    settings.init(known_args)

    filename_suffix = sys.platform
    client_release = 'https://www.dropbox.com/s/m0jqp8i4c6woko5/client?dl=1'
    binary_path = '{}/{}'.format(settings.data_dir, SHELL_LOGGER_BINARY_FILENAME)

    debug('Downloading the shell_logger release and putting it in the path ... ')
    urllib.request.urlretrieve(client_release, binary_path)

    subprocess.Popen(['chmod', '+x', binary_path])

    proc = subprocess.Popen([binary_path, '-mode', 'configure'], stdout=subprocess.PIPE)
    print(''.join([line.decode() for line in proc.stdout.readlines()]))

    try:
        # If process is not running, start the process
        if SHELL_LOGGER_BINARY_FILENAME not in (p.name() for p in psutil.process_iter()):
            os.spawnve(os.P_NOWAIT, binary_path, [binary_path, '-mode', 'daemon'],
                       env={SHELL_LOGGER_SOCKET_ENV_VAR: SHELL_LOGGER_SOCKET_PATH})
    except ZombieProcess as e:
        warn("Zombie process is running. Please kill the running process " % e)


