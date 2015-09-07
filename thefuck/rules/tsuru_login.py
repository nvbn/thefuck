from thefuck import shells
from thefuck.utils import for_app


@for_app('tsuru')
def match(command):
    return ('not authenticated' in command.stderr
            and 'session has expired' in command.stderr)


def get_new_command(command):
    return shells.and_('tsuru login', command.script)
