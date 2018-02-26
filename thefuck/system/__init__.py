import sys


if sys.platform == 'win32':
    from .win32 import *  # noqa: F401,F403
else:
    from .unix import *  # noqa: F401,F403


def get_shell_logger_bname_from_sys():
    """Return the binary name associated with the current system"""
    platform = sys.platform
    if "darwin" in platform:
        return "darwin64"
    elif "linux" in platform:
        return "linux64"
    else:
        return "windows64.exe"
