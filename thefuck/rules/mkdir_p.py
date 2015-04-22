import re

def match(command, settings):
    return ('mkdir' in command.script
            and 'No such file or directory' in command.stderr)


def get_new_command(command, settings):
    return re.sub('^mkdir (.*)', 'mkdir -p \\1', command.script)
