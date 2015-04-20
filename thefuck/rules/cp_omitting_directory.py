def match(command, settings):
    if 'cp: omitting directory' in command.stderr.lower():
        return True
    return False


def get_new_command(command, settings):
    return command.script.replace('cp', 'cp -r') 


