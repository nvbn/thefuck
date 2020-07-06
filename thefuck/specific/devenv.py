from thefuck.utils import which
from subprocess import Popen, PIPE


env_available = bool(which('pyenv')) or bool(which('rbenv')) or bool(which('goenv')) or bool(which('nodenv'))


COMMON_TYPOS = {
    'list': ['versions', 'install --list'],
    'remove': ['uninstall'],
}


def get_commands(app):
    proc = Popen([app, 'commands'], stdout=PIPE)
    return [line.decode('utf-8').strip() for line in proc.stdout.readlines()]
