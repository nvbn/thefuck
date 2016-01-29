"""Package with shell specific actions, each shell class should
implement `from_shell`, `to_shell`, `app_alias`, `put_to_history` and
`get_aliases` methods.
"""
import os
from psutil import Process
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


def _get_shell():
    try:
        shell_name = Process(os.getpid()).parent().name()
    except TypeError:
        shell_name = Process(os.getpid()).parent.name
    return shells.get(shell_name, Generic)()


shell = _get_shell()
