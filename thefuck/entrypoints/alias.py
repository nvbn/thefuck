import six
from ..conf import settings
from ..logs import warn
from ..shells import shell
from ..utils import which


def _get_alias(known_args):
    if six.PY2:
        warn("The Fuck will drop Python 2 support soon, more details "
             "https://github.com/nvbn/thefuck/issues/685")

    if known_args.enable_experimental_instant_mode:
        if six.PY2:
            warn("Instant mode requires Python 3")
        elif not which('script'):
            warn("Instant mode requires `script` app")
        else:
            instant = shell.instant_mode_alias(known_args.alias)
            # Append extras unless this is first-stage logger setup:
            if '--shell-logger' not in instant \
                    and hasattr(shell, 'instant_mode_aliases'):
                try:
                    return shell.instant_mode_aliases(known_args.alias)
                except Exception:
                    return instant
            return instant

    if hasattr(shell, 'app_aliases'):
        try:
            return shell.app_aliases(known_args.alias)
        except Exception:
            pass
    return shell.app_alias(known_args.alias)


def print_alias(known_args):
    settings.init(known_args)
    print(_get_alias(known_args))
