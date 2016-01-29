"""Package with shell specific actions, each shell class should
implement `from_shell`, `to_shell`, `app_alias`, `put_to_history` and
`get_aliases` methods.
"""
import os
import sys
from psutil import Process
from ..utils import memoize
from .. import logs
from .bash import Bash
from .fish import Fish
from .generic import Generic
from .tcsh import Tcsh
from .zsh import Zsh

shells = {'bash': Bash,
          'fish': Fish,
          'zsh': Zsh,
          'csh': Tcsh,
          'tcsh': Tcsh}


@memoize
def _get_shell():
    try:
        shell = Process(os.getpid()).parent().name()
    except TypeError:
        shell = Process(os.getpid()).parent.name
    return shells.get(shell, Generic)()


# Public interface of current shell:
def from_shell(command):
    return _get_shell().from_shell(command)


def to_shell(command):
    return _get_shell().to_shell(command)


def app_alias(alias):
    return _get_shell().app_alias(alias)


def put_to_history(command):
    return _get_shell().put_to_history(command)


def and_(*commands):
    return _get_shell().and_(*commands)


def get_aliases():
    return _get_shell().get_aliases()


def split_command(command):
    return _get_shell().split_command(command)


def quote(s):
    return _get_shell().quote(s)


def get_history():
    return _get_shell().get_history()


def how_to_configure():
    return _get_shell().how_to_configure()
