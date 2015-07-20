from difflib import get_close_matches
from functools import wraps
from pathlib import Path
from shlex import split
import os
import pickle
import re
import six
from .types import Command


DEVNULL = open(os.devnull, 'w')

if six.PY2:
    from pipes import quote
else:
    from shlex import quote


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


def git_support(fn):
    """Resolve git aliases."""
    @wraps(fn)
    def wrapper(command, settings):
        if (command.script.startswith('git') and
                'trace: alias expansion:' in command.stderr):

            search = re.search("trace: alias expansion: ([^ ]*) => ([^\n]*)",
                               command.stderr)
            alias = search.group(1)

            # by default git quotes everything, for example:
            #     'commit' '--amend'
            # which is surprising and does not allow to easily test for
            # eg. 'git commit'
            expansion = ' '.join(map(quote, split(search.group(2))))
            new_script = command.script.replace(alias, expansion)

            command = Command._replace(command, script=new_script)
        return fn(command, settings)

    return wrapper


def memoize(fn):
    """Caches previous calls to the function."""
    memo = {}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = pickle.dumps((args, kwargs))
        if key not in memo or memoize.disabled:
            memo[key] = fn(*args, **kwargs)

        return memo[key]

    return wrapper
memoize.disabled = False


def get_closest(word, possibilities, n=3, cutoff=0.6, fallback_to_first=True):
    """Returns closest match or just first from possibilities."""
    possibilities = list(possibilities)
    try:
        return get_close_matches(word, possibilities, n, cutoff)[0]
    except IndexError:
        if fallback_to_first:
            return possibilities[0]


@memoize
def get_all_executables():
    from thefuck.shells import thefuck_alias, get_aliases

    def _safe(fn, fallback):
        try:
            return fn()
        except OSError:
            return fallback

    tf_alias = thefuck_alias()
    return [exe.name
            for path in os.environ.get('PATH', '').split(':')
            for exe in _safe(lambda: list(Path(path).iterdir()), [])
            if not _safe(exe.is_dir, True)] + [
                alias for alias in get_aliases() if alias != tf_alias]
