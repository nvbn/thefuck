from thefuck.utils import which


env_available = bool(which('pyenv')) or bool(which('rbenv')) or bool(which('goenv')) or bool(which('nodenv'))


COMMON_TYPOS = {
    'list': ['versions', 'install --list'],
    'remove': ['uninstall'],
}
