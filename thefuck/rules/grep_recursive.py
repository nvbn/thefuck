from thefuck.utils import for_app


@for_app('grep')
def match(command, settings):
    return 'is a directory' in command.stderr.lower()


def get_new_command(command, settings):
    return 'grep -r {}'.format(command.script[5:])
