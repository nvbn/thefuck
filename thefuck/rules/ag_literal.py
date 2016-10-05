from thefuck.utils import for_app


@for_app('ag')
def match(command):
    return 'run ag with -Q' in command.stderr


def get_new_command(command):
    return command.script.replace('ag', 'ag -Q', 1)
