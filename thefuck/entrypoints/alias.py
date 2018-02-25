import subprocess
import urllib.request

import sys
import six
import psutil

from ..conf import settings
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


def print_experimental_shell_history():
    filename_suffix = sys.platform
    client_release = 'https://www.dropbox.com/s/m0jqp8i4c6woko5/client?dl=1'
    filename = settings.env['__SHELL_LOGGER_BINARY_PATH']
    debug('Downloading the shell_logger release and putting it in the path ... ')
    urllib.request.urlretrieve(client_release, filename)

    subprocess.Popen(['chmod', '+x', filename])

    proc = subprocess.Popen(['./{0}'.format(filename), '-mode', 'configure'], stdout=subprocess.PIPE,
                            env={'__SHELL_LOGGER_BINARY_PATH': settings.env['__SHELL_LOGGER_BINARY_PATH']})
    print(''.join([line.decode() for line in proc.stdout.readlines()]))

    # If process is running, close it
    if filename in (p.name() for p in psutil.process_iter()):
        subprocess.Popen(['./{0}'.format(filename), '-mode', 'daemon'])
        subprocess.Popen(['rm', './{0}'.format(filename)])

    subprocess.Popen(['./{0}'.format(filename), '-mode', 'daemon'],
                     env={'__SHELL_LOGGER_SOCKET': settings.env['__SHELL_LOGGER_SOCKET']})
