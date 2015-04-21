import os


def match(command, settings):
    return os.path.exists(command.script.split()[0]) \
        and 'command not found' in command.stderr


def get_new_command(command, settings):
    return u'./{}'.format(command.script)

