import os
import subprocess
from ..utils import memoize, which

BREW_CMD_PATH = '/Library/Homebrew/cmd'
TAP_PATH = '/Library/Taps'
TAP_CMD_PATH = '/%s/%s/cmd'

brew_available = bool(which('brew'))


@memoize
def get_brew_path_prefix():
    """To get brew path"""
    try:
        return subprocess.check_output(['brew', '--prefix'],
                                       universal_newlines=True).strip()
    except Exception:
        return None


def get_brew_commands(brew_path_prefix):
    """To get brew default commands on local environment"""
    brew_cmd_path = brew_path_prefix + BREW_CMD_PATH

    return [name[:-3] for name in os.listdir(brew_cmd_path)
            if name.endswith(('.rb', '.sh'))]


def get_brew_tap_specific_commands(brew_path_prefix):
    def _is_brew_tap_cmd_naming(name):
        return name.startswith('brew-') and name.endswith('.rb')

    def _get_directory_names_only(path):
        return [d for d in os.listdir(path)
                if os.path.isdir(os.path.join(path, d))]

    """To get tap's specific commands
    https://github.com/Homebrew/homebrew/blob/master/Library/brew.rb#L115"""
    commands = []
    brew_taps_path = brew_path_prefix + TAP_PATH

    for user in _get_directory_names_only(brew_taps_path):
        taps = _get_directory_names_only(brew_taps_path + '/%s' % user)

        # Brew Taps's naming rule
        # https://github.com/Homebrew/homebrew/blob/master/share/doc/homebrew/brew-tap.md#naming-conventions-and-limitations
        taps = (tap for tap in taps if tap.startswith('homebrew-'))
        for tap in taps:
            tap_cmd_path = brew_taps_path + TAP_CMD_PATH % (user, tap)

            if os.path.isdir(tap_cmd_path):
                commands += (name.replace('brew-', '').replace('.rb', '')
                             for name in os.listdir(tap_cmd_path)
                             if _is_brew_tap_cmd_naming(name))

    return commands


def all_brew_commands():
    brew_path_prefix = get_brew_path_prefix()
    if brew_path_prefix:
        try:
            return (get_brew_commands(brew_path_prefix)
                    + get_brew_tap_specific_commands(brew_path_prefix))
        except OSError:
            pass

    # Failback commands for testing (Based on Homebrew 0.9.5)
    return ['info', 'home', 'options', 'install', 'uninstall',
            'search', 'list', 'update', 'upgrade', 'pin', 'unpin',
            'doctor', 'create', 'edit']
