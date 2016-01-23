from collections import defaultdict
from psutil import Process
import os
import sys
from ..utils import memoize
from .. import logs
from .bash import Bash
from .fish import Fish
from .generic import Generic
from .tcsh import Tcsh
from .zsh import Zsh

shells = defaultdict(Generic,
                     bash=Bash(),
                     fish=Fish(),
                     zsh=Zsh(),
                     csh=Tcsh(),
                     tcsh=Tcsh())


@memoize
def _get_shell():
    try:
        shell = Process(os.getpid()).parent().name()
    except TypeError:
        shell = Process(os.getpid()).parent.name
    return shells[shell]


def from_shell(command):
    return _get_shell().from_shell(command)


def to_shell(command):
    return _get_shell().to_shell(command)


def app_alias(alias):
    return _get_shell().app_alias(alias)


def thefuck_alias():
    return os.environ.get('TF_ALIAS', 'fuck')


def put_to_history(command):
    try:
        return _get_shell().put_to_history(command)
    except IOError:
        logs.exception("Can't update history", sys.exc_info())


def and_(*commands):
    return _get_shell().and_(*commands)


def get_aliases():
    return list(_get_shell().get_aliases().keys())


def split_command(command):
    return _get_shell().split_command(command)


def quote(s):
    return _get_shell().quote(s)


@memoize
def get_history():
    return list(_get_shell().get_history())


def how_to_configure():
    return _get_shell().how_to_configure()
