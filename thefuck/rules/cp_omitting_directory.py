import re
from thefuck.utils import sudo_support


@sudo_support
def match(command, settings):
    return command.script.startswith('cp ') \
        and 'cp: omitting directory' in command.stderr.lower()


@sudo_support
def get_new_command(command, settings):
    return re.sub(r'^cp', 'cp -a', command.script)
