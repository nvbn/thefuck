from thefuck.utils import for_app


@for_app('ls')
def match(command, settings):
    return 'ls -' not in command.script


def get_new_command(command, settings):
    command = command.script.split(' ')
    command[0] = 'ls -lah'
    return ' '.join(command)
