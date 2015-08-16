from .types import Command
from difflib import get_close_matches
from functools import wraps
from pathlib import Path
from shlex import split
import os
import pickle
import re
import six


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
        elif isinstance(result, list):
            return [u'sudo {}'.format(x) for x in result]
        else:
            return result
    return wrapper


def git_support(fn):
    """Resolves git aliases and supports testing for both git and hub."""
    @wraps(fn)
    def wrapper(command, settings):
        # supports GitHub's `hub` command
        # which is recommended to be used with `alias git=hub`
        # but at this point, shell aliases have already been resolved
        is_git_cmd = command.script.startswith(('git', 'hub'))

        if not is_git_cmd:
            return False

        # perform git aliases expansion
        if 'trace: alias expansion:' in command.stderr:
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


def replace_argument(script, from_, to):
    """Replaces command line argument."""
    replaced_in_the_end = re.sub(u' {}$'.format(from_), u' {}'.format(to),
                                 script, count=1)
    if replaced_in_the_end != script:
        return replaced_in_the_end
    else:
        return script.replace(
            u' {} '.format(from_), u' {} '.format(to), 1)


def eager(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return list(fn(*args, **kwargs))
    return wrapper


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
