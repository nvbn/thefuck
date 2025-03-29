import sys


if sys.platform == 'win32':
    from .win32 import *  # noqa: F401,F403
else:
    from .unix import *  # noqa: F401,F403
