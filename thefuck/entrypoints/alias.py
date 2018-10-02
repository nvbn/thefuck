import subprocess
import urllib.request

import os
import sys
import six
import psutil
from psutil import ZombieProcess

from ..conf import settings
from ..system import get_shell_logger_bname_from_sys
from ..const import SHELL_LOGGER_SOCKET_ENV_VAR, SHELL_LOGGER_SOCKET_PATH, \
                    SHELL_LOGGER_BINARY_FILENAME, SHELL_LOGGER_DB_FILENAME, SHELL_LOGGER_DB_ENV_VAR
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

    filename_suffix = get_shell_logger_bname_from_sys()
    client_release = 'https://github.com/nvbn/shell_logger/releases/download/0.1.0a1/shell_logger_{}'\
                     .format(filename_suffix)
    binary_path = '{}/{}'.format(settings.data_dir, SHELL_LOGGER_BINARY_FILENAME)
    db_path = '{}/{}'.format(settings.data_dir, SHELL_LOGGER_DB_FILENAME)

    debug('Downloading the shell_logger release and putting it in the path ... ')
    urllib.request.urlretrieve(client_release, binary_path)

    subprocess.Popen(['chmod', '+x', binary_path])

    my_env = os.environ.copy()
    my_env[SHELL_LOGGER_DB_ENV_VAR] = db_path
    proc = subprocess.Popen([binary_path, '-mode', 'configure'], stdout=subprocess.PIPE,
                            env=my_env)
    print(''.join([line.decode() for line in proc.stdout.readlines()]))
    # TODO seems like daemon returns something, so redirect stdout so eval doesn't hang
    subprocess.Popen(["{} -mode daemon &".format(binary_path)], shell=True,
                               env={SHELL_LOGGER_SOCKET_ENV_VAR: SHELL_LOGGER_SOCKET_PATH,
                                    SHELL_LOGGER_DB_ENV_VAR: db_path}, stdout=2)


