from thefuck.shells import shell
from thefuck.utils import for_app


@for_app('rbenv')
def match(command):
    return ('ruby-build: definition not found' in command.output.lower() and
            'if the version you need is missing, try upgrading ruby-build' in command.output.lower()
            )


def get_new_command(command):
    actualCommand = command.output.split('\n')[-1].lstrip()
    return shell.to_shell(actualCommand)
