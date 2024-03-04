def match(command):
    if command.script_parts and '&&' not in command.script_parts and command.script_parts[0] == 'su':
        return False

    return 'command not found: sudo' in command.output.lower()


def get_new_command(command):
    return u'su -c "{}"'.format(command.script.replace('"', '\\"').replace('sudo ', ''))


priority = 1200
