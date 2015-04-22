import re
from thefuck.utils import sudo_support


@sudo_support
def match(command, settings):
    return ('mkdir' in command.script
            and 'No such file or directory' in command.stderr)


@sudo_support
def get_new_command(command, settings):
    return re.sub('^mkdir (.*)', 'mkdir -p \\1', command.script)
