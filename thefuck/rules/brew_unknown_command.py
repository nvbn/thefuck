import difflib
import re
import thefuck.logs

# This commands are based on Homebrew 0.9.5
brew_commands = ['info', 'home', 'options', 'install', 'uninstall', 'search',
                 'list', 'update', 'upgrade', 'pin', 'unpin', 'doctor',
                 'create', 'edit']


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
