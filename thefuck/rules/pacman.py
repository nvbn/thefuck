from thefuck.archlinux import archlinux_env, get_pkgfile
from thefuck import shells


def match(command, settings):
    return 'not found' in command.stderr and get_pkgfile(command)


def get_new_command(command, settings):
    packages = get_pkgfile(command)

    formatme = shells.and_('{} -S {}', '{}')
    return [formatme.format(pacman, package, command.script)
            for package in packages]

enabled_by_default, pacman = archlinux_env()
