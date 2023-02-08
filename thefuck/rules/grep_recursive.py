from thefuck.utils import for_app


@for_app('grep')
def match(command):
    return 'is a directory' in command.output.lower()


def get_new_command(command):
    return f'grep -r {command.script[5:]}'
