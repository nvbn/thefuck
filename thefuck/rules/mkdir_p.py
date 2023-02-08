import re

from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command):
    return ('mkdir' in command.script
            and 'No such file or directory' in command.output)


@sudo_support
def get_new_command(command):
    return re.sub('\\bmkdir (.*)', 'mkdir -p \\1', command.script)
