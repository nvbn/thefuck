def match(command):
    return (command.script.startswith(u'man')
            and u'command not found' in command.stderr.lower())


def get_new_command(command):
    return u'man {}'.format(command.script[3:])

priority = 2000
