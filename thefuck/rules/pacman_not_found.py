""" Fixes wrong package names with pacman or yaourt.

For example the `llc` program is in package `llvm` so this:
    yaourt -S llc
should be:
    yaourt -S llvm
"""

from thefuck.utils import replace_command, get_pkgfile, archlinux_env


def match(command, settings):
    return (command.script.startswith(('pacman', 'sudo pacman', 'yaourt'))
            and 'error: target not found:' in command.stderr)


def get_new_command(command, settings):
    pgr = command.script.split()[-1]

    return replace_command(command, pgr, get_pkgfile(pgr))


enabled_by_default, _ = archlinux_env()
