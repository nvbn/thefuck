import re


def match(command, settings):
    return command.script.startswith('cp ') \
        and 'cp: omitting directory' in command.stderr.lower()


def get_new_command(command, settings):
    return re.sub(r'^cp', 'cp -a', command.script)
