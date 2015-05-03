import difflib
import os
import re
import subprocess


BREW_CMD_PATH = '/Library/Homebrew/cmd'
TAP_PATH = '/Library/Taps'
TAP_CMD_PATH = '/%s/%s/cmd'


def _get_brew_path_prefix():
    """To get brew path"""
    try:
        return subprocess.check_output(['brew', '--prefix']).strip()
    except:
        return None


def _get_brew_commands(brew_path_prefix):
    """To get brew default commands on local environment"""
    brew_cmd_path = brew_path_prefix + BREW_CMD_PATH

    commands = [name.replace('.rb', '') for name in os.listdir(brew_cmd_path)
                if name.endswith('.rb')]

    return commands


def _get_brew_tap_specific_commands(brew_path_prefix):
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


def _is_brew_tap_cmd_naming(name):
    if name.startswith('brew-') and name.endswith('.rb'):
        return True

    return False


def _get_directory_names_only(path):
    return [d for d in os.listdir(path)
            if os.path.isdir(os.path.join(path, d))]


brew_path_prefix = _get_brew_path_prefix()

# Failback commands for testing (Based on Homebrew 0.9.5)
brew_commands = ['info', 'home', 'options', 'install', 'uninstall',
                 'search', 'list', 'update', 'upgrade', 'pin', 'unpin',
                 'doctor', 'create', 'edit']

if brew_path_prefix:
    try:
        brew_commands = _get_brew_commands(brew_path_prefix) \
                        + _get_brew_tap_specific_commands(brew_path_prefix)
    except OSError:
        pass


def _get_similar_commands(command):
    return difflib.get_close_matches(command, brew_commands)


def match(command, settings):
    is_proper_command = ('brew' in command.script and
                         'Unknown command' in command.stderr)

    has_possible_commands = False
    if is_proper_command:
        broken_cmd = re.findall(r'Error: Unknown command: ([a-z]+)',
                                command.stderr)[0]
        has_possible_commands = len(_get_similar_commands(broken_cmd)) > 0

    return has_possible_commands


def get_new_command(command, settings):
    broken_cmd = re.findall(r'Error: Unknown command: ([a-z]+)',
                            command.stderr)[0]
    new_cmd = _get_similar_commands(broken_cmd)[0]

    return command.script.replace(broken_cmd, new_cmd, 1)
