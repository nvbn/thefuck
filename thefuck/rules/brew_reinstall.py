import re

from thefuck.utils import for_app

warning_regex = re.compile(r'Warning: (?:.(?!is ))+ is already installed and '
                           r'up-to-date')
message_regex = re.compile(r'To reinstall (?:(?!, ).)+, run `brew reinstall '
                           r'[^`]+`')


@for_app('brew', at_least=2)
def match(command):
    return ('install' in command.script
            and warning_regex.search(command.output)
            and message_regex.search(command.output))


def get_new_command(command):
    return command.script.replace('install', 'reinstall')
