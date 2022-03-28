""" Fixes wrong package names with pacman or yaourt.

For example the `llc` program is in package `llvm` so this:
    yay -S llc
should be:
    yay -S llvm
"""

from thefuck.utils import for_app, replace_command
from thefuck.specific.archlinux import get_pkgfile, archlinux_env
from thefuck.specific.sudo import sudo_support


@sudo_support
@for_app('pacman', 'pikaur', 'yaourt', 'yay')
def match(command):
    return 'error: target not found:' in command.output


def get_new_command(command):
    pgr = command.script_parts[-1]

    return replace_command(command, pgr, get_pkgfile(pgr))


enabled_by_default, _ = archlinux_env()
