def match(command):
    return command.script.endswith('ç')

def get_new_command(command):
    return command.script[:-1]

