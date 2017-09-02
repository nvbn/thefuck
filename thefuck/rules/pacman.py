from thefuck.specific.archlinux import get_pkgfile, archlinux_env
from thefuck.shells import shell


def match(command):
    return 'not found' in command.output and get_pkgfile(command.script)


def get_new_command(command):
    packages = get_pkgfile(command.script)

    formatme = shell.and_('{} -S {}', '{}')
    return [formatme.format(pacman, package, command.script)
            for package in packages]


enabled_by_default, pacman = archlinux_env()
