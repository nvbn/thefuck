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
from .powershell import Powershell

shells = {'bash': Bash,
          'fish': Fish,
          'zsh': Zsh,
          'csh': Tcsh,
          'tcsh': Tcsh,
          'powershell': Powershell}


def _get_shell():
    proc = Process(os.getpid())

    while proc is not None and proc.pid > 0:
        try:
            name = proc.name()
        except TypeError:
            name = proc.name

        name = os.path.splitext(name)[0]

        if name in shells:
            return shells[name]()

        try:
            proc = proc.parent()
        except TypeError:
            proc = proc.parent

    return Generic()


shell = _get_shell()
