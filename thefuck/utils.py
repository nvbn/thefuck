import os
import pickle
import pkg_resources
import re
import shelve
import six
from contextlib import closing
from decorator import decorator
from difflib import get_close_matches
from functools import wraps
from warnings import warn
from .conf import settings
from .system import Path

DEVNULL = open(os.devnull, 'w')

if six.PY2:
    import anydbm
    shelve_open_error = anydbm.error
else:
    import dbm
    shelve_open_error = dbm.error


def memoize(fn):
    """Caches previous calls to the function."""
    memo = {}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not memoize.disabled:
            key = pickle.dumps((args, kwargs))
            if key not in memo:
                memo[key] = fn(*args, **kwargs)
            value = memo[key]
        else:
            # Memoize is disabled, call the function
            value = fn(*args, **kwargs)

        return value

    return wrapper
memoize.disabled = False


@memoize
def which(program):
    """Returns `program` path or `None`."""
    try:
        from shutil import which

        return which(program)
    except ImportError:
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


def default_settings(params):
    """Adds default values to settings if it not presented.

    Usage:

        @default_settings({'apt': '/usr/bin/apt'})
        def match(command, settings):
            print(settings.apt)

    """
    def _default_settings(fn, command):
        for k, w in params.items():
            settings.setdefault(k, w)
        return fn(command)
    return decorator(_default_settings)


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
    from thefuck.shells import shell

    def _safe(fn, fallback):
        try:
            return fn()
        except OSError:
            return fallback

    tf_alias = get_alias()
    tf_entry_points = get_installation_info().get_entry_map()\
                                             .get('console_scripts', {})\
                                             .keys()
    bins = [exe.name.decode('utf8') if six.PY2 else exe.name
            for path in os.environ.get('PATH', '').split(':')
            for exe in _safe(lambda: list(Path(path).iterdir()), [])
            if not _safe(exe.is_dir, True)
            and exe.name not in tf_entry_points]
    aliases = [alias for alias in shell.get_aliases() if alias != tf_alias]
    return bins + aliases


def replace_argument(script, from_, to):
    """Replaces command line argument."""
    replaced_in_the_end = re.sub(u' {}$'.format(re.escape(from_)), u' {}'.format(to),
                                 script, count=1)
    if replaced_in_the_end != script:
        return replaced_in_the_end
    else:
        return script.replace(
            u' {} '.format(from_), u' {} '.format(to), 1)


@decorator
def eager(fn, *args, **kwargs):
    return list(fn(*args, **kwargs))


@eager
def get_all_matched_commands(stderr, separator='Did you mean'):
    should_yield = False
    for line in stderr.split('\n'):
        if separator in line:
            should_yield = True
        elif should_yield and line:
            yield line.strip()


def replace_command(command, broken, matched):
    """Helper for *_no_command rules."""
    new_cmds = get_close_matches(broken, matched, cutoff=0.1)
    return [replace_argument(command.script, broken, new_cmd.strip())
            for new_cmd in new_cmds]


@memoize
def is_app(command, *app_names, **kwargs):
    """Returns `True` if command is call to one of passed app names."""

    at_least = kwargs.pop('at_least', 0)
    if kwargs:
        raise TypeError("got an unexpected keyword argument '{}'".format(kwargs.keys()))

    if len(command.script_parts) > at_least:
        return command.script_parts[0] in app_names

    return False


def for_app(*app_names, **kwargs):
    """Specifies that matching script is for on of app names."""
    def _for_app(fn, command):
        if is_app(command, *app_names, **kwargs):
            return fn(command)
        else:
            return False

    return decorator(_for_app)


def cache(*depends_on):
    """Caches function result in temporary file.

    Cache will be expired when modification date of files from `depends_on`
    will be changed.

    Function wrapped in `cache` should be arguments agnostic.

    """
    def _get_mtime(name):
        path = os.path.join(os.path.expanduser('~'), name)
        try:
            return str(os.path.getmtime(path))
        except OSError:
            return '0'

    def _get_cache_path():
        default_xdg_cache_dir = os.path.expanduser("~/.cache")
        cache_dir = os.getenv("XDG_CACHE_HOME", default_xdg_cache_dir)
        cache_path = Path(cache_dir).joinpath('thefuck').as_posix()

        # Ensure the cache_path exists, Python 2 does not have the exist_ok
        # parameter
        try:
            os.makedirs(cache_dir)
        except OSError:
            if not os.path.isdir(cache_dir):
                raise

        return cache_path

    @decorator
    def _cache(fn, *args, **kwargs):
        if cache.disabled:
            return fn(*args, **kwargs)

        # A bit obscure, but simplest way to generate unique key for
        # functions and methods in python 2 and 3:
        key = '{}.{}'.format(fn.__module__, repr(fn).split('at')[0])

        etag = '.'.join(_get_mtime(name) for name in depends_on)
        cache_path = _get_cache_path()

        try:
            with closing(shelve.open(cache_path)) as db:
                if db.get(key, {}).get('etag') == etag:
                    return db[key]['value']
                else:
                    value = fn(*args, **kwargs)
                    db[key] = {'etag': etag, 'value': value}
                    return value
        except (shelve_open_error, ImportError):
            # Caused when switching between Python versions
            warn("Removing possibly out-dated cache")
            os.remove(cache_path)

            with closing(shelve.open(cache_path)) as db:
                value = fn(*args, **kwargs)
                db[key] = {'etag': etag, 'value': value}
                return value

    return _cache
cache.disabled = False


def get_installation_info():
    return pkg_resources.require('thefuck')[0]


def get_alias():
    return os.environ.get('TF_ALIAS', 'fuck')


@memoize
def get_valid_history_without_current(command):
    def _not_corrected(history, tf_alias):
        """Returns all lines from history except that comes before `fuck`."""
        previous = None
        for line in history:
            if previous is not None and line != tf_alias:
                yield previous
            previous = line
        if history:
            yield history[-1]

    from thefuck.shells import shell
    history = shell.get_history()
    tf_alias = get_alias()
    executables = set(get_all_executables())
    return [line for line in _not_corrected(history, tf_alias)
            if not line.startswith(tf_alias) and not line == command.script
            and line.split(' ')[0] in executables]
