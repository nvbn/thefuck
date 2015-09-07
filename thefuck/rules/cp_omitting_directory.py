import re
from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app


@sudo_support
@for_app('cp')
def match(command):
    stderr = command.stderr.lower()
    return 'omitting directory' in stderr or 'is a directory' in stderr


@sudo_support
def get_new_command(command):
    return re.sub(r'^cp', 'cp -a', command.script)
