def match(command):
    if command.script_parts and '&&' not in command.script_parts and command.script_parts[0] == 'su':
        return False

    return 'command not found: sudo' in command.output.lower()


def get_new_command(command):
    if '&&' in command.script:
        return u'su -c "sh -c "{}""'.format(" ".join([part for part in command.script_parts if part != "sudo"]))
    elif '>' in command.script:
        return u'su -c "sh -c "{}""'.format(command.script.replace('"', '\\"'))
    else:
        return u'su -c {}'.format(command.script)
priority = 1200
