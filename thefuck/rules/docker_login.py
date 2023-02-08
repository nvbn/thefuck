from thefuck.shells import shell
from thefuck.utils import for_app


@for_app('docker')
def match(command):
    return ('docker' in command.script
            and "access denied" in command.output
            and "may require 'docker login'" in command.output)


def get_new_command(command):
    return shell.and_('docker login', command.script)
