from thefuck.utils import for_app


@for_app('ls')
def match(command):
    return command.split_script and 'ls -' not in command.script


def get_new_command(command):
    command = command.split_script[:]
    command[0] = 'ls -lah'
    return ' '.join(command)
