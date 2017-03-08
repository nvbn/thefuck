from thefuck.utils import for_app


@for_app('ag')
def match(command):
    return command.stderr.endswith('run ag with -Q\n')


def get_new_command(command):
    return command.script.replace('ag', 'ag -Q', 1)
