import atexit
import os
import pickle
import re
import shelve
import six
import sys
from decorator import decorator
from difflib import get_close_matches
from functools import wraps
from .logs import warn
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
        def match(command):
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
    tf_entry_points = ['thefuck', 'fuck']

    bins = [exe.name.decode('utf8') if six.PY2 else exe.name
            for path in os.environ.get('PATH', '').split(os.pathsep)
            for exe in _safe(lambda: list(Path(path).iterdir()), [])
            if not _safe(exe.is_dir, True)
            and exe.name not in tf_entry_points]
    aliases = [alias.decode('utf8') if six.PY2 else alias
               for alias in shell.get_aliases() if alias != tf_alias]

    win32 = sys.platform.startswith('win')
    if win32:
        bins += [exe[:-4] for exe in bins if exe.endswith(".exe")]

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
    if not isinstance(separator, list):
        separator = [separator]
    should_yield = False
    for line in stderr.split('\n'):
        for sep in separator:
            if sep in line:
                should_yield = True
                break
        else:
            if should_yield and line:
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


class Cache(object):
    """Lazy read cache and save changes at exit."""

    def __init__(self):
        self._db = None

    def _init_db(self):
        cache_dir = self._get_cache_dir()
        cache_path = Path(cache_dir).joinpath('thefuck').as_posix()

        try:
            self._db = shelve.open(cache_path)
        except shelve_open_error + (ImportError,):
            # Caused when switching between Python versions
            warn("Removing possibly out-dated cache")
            os.remove(cache_path)
            self._db = shelve.open(cache_path)

        atexit.register(self._db.close)

    def _get_cache_dir(self):
        default_xdg_cache_dir = os.path.expanduser("~/.cache")
        cache_dir = os.getenv("XDG_CACHE_HOME", default_xdg_cache_dir)

        # Ensure the cache_path exists, Python 2 does not have the exist_ok
        # parameter
        try:
            os.makedirs(cache_dir)
        except OSError:
            if not os.path.isdir(cache_dir):
                raise

        return cache_dir

    def _get_mtime(self, path):
        try:
            return str(os.path.getmtime(path))
        except OSError:
            return '0'

    def _get_key(self, fn, depends_on, args, kwargs):
        parts = (fn.__module__, repr(fn).split('at')[0],
                 depends_on, args, kwargs)
        return str(pickle.dumps(parts))

    def get_value(self, fn, depends_on, args, kwargs):
        if self._db is None:
            self._init_db()

        depends_on = [Path(name).expanduser().absolute().as_posix()
                      for name in depends_on]
        key = self._get_key(fn, depends_on, args, kwargs)
        etag = '.'.join(self._get_mtime(path) for path in depends_on)

        if self._db.get(key, {}).get('etag') == etag:
            return self._db[key]['value']
        else:
            value = fn(*args, **kwargs)
            self._db[key] = {'etag': etag, 'value': value}
            return value


_cache = Cache()


def cache(*depends_on):
    """Caches function result in temporary file.

    Cache will be expired when modification date of files from `depends_on`
    will be changed.

    Only functions should be wrapped in `cache`, not methods.

    """
    def cache_decorator(fn):
        @memoize
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if cache.disabled:
                return fn(*args, **kwargs)
            else:
                return _cache.get_value(fn, depends_on, args, kwargs)

        return wrapper

    return cache_decorator


cache.disabled = False


def get_installation_info():
    import pkg_resources

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
    executables = set(get_all_executables())\
        .union(shell.get_builtin_commands())

    return [line for line in _not_corrected(history, tf_alias)
            if not line.startswith(tf_alias) and not line == command.script
            and line.split(' ')[0] in executables]


def format_raw_script(raw_script):
    """Creates single script from a list of script parts.

    :type raw_script: [basestring]
    :rtype: basestring

    """
    if six.PY2:
        script = ' '.join(arg.decode('utf-8') for arg in raw_script)
    else:
        script = ' '.join(raw_script)

    return script.strip()
