def match(command):
    return command.script.isupper()


def get_new_command(command):
    return command.script.lower()

priority = 0
