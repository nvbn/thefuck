import six
from ..logs import warn
from ..shells import shell


def print_alias(known_args):
    if six.PY2:
        warn("The Fuck will drop Python 2 support soon, more details "
             "https://github.com/nvbn/thefuck/issues/685")

    if known_args.enable_experimental_instant_mode:
        if six.PY2:
            warn("Instant mode not supported with Python 2")
            alias = shell.app_alias(known_args.alias)
        else:
            alias = shell.instant_mode_alias(known_args.alias)
    else:
        alias = shell.app_alias(known_args.alias)

    print(alias)
