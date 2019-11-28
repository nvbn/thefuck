import re
from thefuck.utils import for_app


warning_regex = re.compile(r'Warning: Cask \'(?:.(?!is ))+\' is already installed.\n\n')
message_regex = re.compile(r'To re-install (?:(?!, ).)+, run\n  `brew cask reinstall [^`]+`')


@for_app('brew', at_least=2)
def match(command):
    return ('cask install' in command.script
            and warning_regex.search(command.output)
            and message_regex.search(command.output))


def get_new_command(command):
    return command.script.replace('install', 'reinstall')
