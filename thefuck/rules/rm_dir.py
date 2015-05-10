import re
from thefuck.utils import sudo_support


@sudo_support
def match(command, settings):
    return ('rm' in command.script
            and 'is a directory' in command.stderr.lower())


@sudo_support
def get_new_command(command, settings):
    return re.sub('^rm (.*)', 'rm -rf \\1', command.script)
