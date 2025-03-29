from thefuck.utils import for_app


@for_app('grep')
def match(command):
    return 'is a directory' in command.output.lower()


def get_new_command(command):
    return u'grep -r {}'.format(command.script[5:])
