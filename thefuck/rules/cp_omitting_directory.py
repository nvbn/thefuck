import re
from thefuck.utils import sudo_support


@sudo_support
def match(command, settings):
    stderr = command.stderr.lower()
    return command.script.startswith('cp ') \
        and ('omitting directory' in stderr or 'is a directory' in stderr)


@sudo_support
def get_new_command(command, settings):
    return re.sub(r'^cp', 'cp -a', command.script)
