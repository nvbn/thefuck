import re

def match(command, settings):
    return ('rmdir' in command.script
            and 'Directory not empty' in command.stderr)


def get_new_command(command, settings):
    return re.sub('^rm (.*)', 'rm -rf \\1', command.script)
