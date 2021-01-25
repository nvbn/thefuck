import six
from ..logs import warn
from ..shells import shell
from ..utils import which
from collections import Iterable


def _warn_py2(known_args):
    if six.PY2:
        warn("The Fuck will drop Python 2 support soon, more details "
             "https://github.com/nvbn/thefuck/issues/685")



def _get_alias(known_args):
    _warn_py2(known_args)

    if known_args.enable_experimental_instant_mode:
        if six.PY2:
            warn("Instant mode requires Python 3")
        elif not which('script'):
            warn("Instant mode requires `script` app")
        else:
            return shell.instant_mode_alias(known_args.alias)

    return shell.app_alias(known_args.alias)


def _print_alias_multi(known_args):
    _warn_py2(known_args)
    if known_args.enable_experimental_instant_mode:
        if six.PY2:
            warn("Instant mode requires Python 3")
        elif not which('script'):
            warn("Instant mode requires `script` app")
        else:
            for a in known_args.alias:
                print(shell.instant_mode_alias(a))
    else:
        for a in known_args.alias:
            print(shell.app_alias(a))


def print_alias(known_args):
    if isinstance(shell.app_alias(known_args), Iterable):
        _print_alias_multi(known_args)
    else:
        print(_get_alias(known_args))
