import sys


if sys.platform == 'win32':
    from .win32 import *
else:
    from .unix import *
