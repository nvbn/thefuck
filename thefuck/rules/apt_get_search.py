import re


def match(command, settings):
    return command.script.startswith('apt-get search')


def get_new_command(command, settings):
    return re.sub(r'^apt-get', 'apt-cache', command.script)
