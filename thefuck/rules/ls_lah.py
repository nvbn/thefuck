def match(command, settings):
    return (command.script == 'ls'
            or command.script.startswith('ls ')
            and 'ls -' not in command.script)


def get_new_command(command, settings):
    command = command.script.split(' ')
    command[0] = 'ls -lah'
    return ' '.join(command)
