import os
import msvcrt
import warnings
import win_unicode_console
from .. import const


def init_output():
    import colorama
    # Suppress RuntimeWarning from win_unicode_console when stdin/stdout
    # encodings differ (common on Windows with non-English locales).
    # See: https://github.com/nvbn/thefuck/issues/514
    #      https://github.com/nvbn/thefuck/issues/673
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"sys\.stdin\.encoding",
            category=RuntimeWarning
        )
        win_unicode_console.enable()
    colorama.init()


def get_key():
    ch = msvcrt.getwch()
    if ch in ('\x00', '\xe0'):  # arrow or function key prefix?
        ch = msvcrt.getwch()  # second call returns the actual key code

    if ch in const.KEY_MAPPING:
        return const.KEY_MAPPING[ch]
    if ch == 'H':
        return const.KEY_UP
    if ch == 'P':
        return const.KEY_DOWN

    return ch


def open_command(arg):
    return 'cmd /c start ' + arg


try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


def _expanduser(self):
    return self.__class__(os.path.expanduser(str(self)))


# pathlib's expanduser fails on windows, see http://bugs.python.org/issue19776
Path.expanduser = _expanduser
