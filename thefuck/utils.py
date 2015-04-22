from functools import wraps
import os
import six
from .types import Command


def which(program):
    """Returns `program` path or `None`."""

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def wrap_settings(params):
    """Adds default values to settings if it not presented.

    Usage:

        @wrap_settings({'apt': '/usr/bin/apt'})
        def match(command, settings):
            print(settings.apt)

    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(command, settings):
            return fn(command, settings.update(**params))
        return wrapper
    return decorator


def sudo_support(fn):
    """Removes sudo before calling fn and adds it after."""
    @wraps(fn)
    def wrapper(command, settings):
        if not command.script.startswith('sudo '):
            return fn(command, settings)

        result = fn(Command(command.script[5:],
                            command.stdout,
                            command.stderr),
                    settings)

        if result and isinstance(result, six.string_types):
            return u'sudo {}'.format(result)
        else:
            return result
    return wrapper
