""" Fixes wrong package names with pacman or yaourt.

For example the `llc` program is in package `llvm` so this:
    yaourt -S llc
should be:
    yaourt -S llvm
"""

from thefuck.utils import replace_command
from thefuck.specific.archlinux import get_pkgfile, archlinux_env


def match(command):
    return (command.script.startswith(('pacman', 'sudo pacman', 'yaourt'))
            and 'error: target not found:' in command.stderr)


def get_new_command(command):
    pgr = command.script.split()[-1]

    return replace_command(command, pgr, get_pkgfile(pgr))


enabled_by_default, _ = archlinux_env()
