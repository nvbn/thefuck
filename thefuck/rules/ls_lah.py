def match(command, settings):
    return 'ls' in command.script and not ('ls -' in command.script)


def get_new_command(command, settings):
    command = command.script.split(' ')
    command[0] = 'ls -lah'
    return ' '.join(command)
