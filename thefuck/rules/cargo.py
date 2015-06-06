def match(command, settings):
    return command.script == 'cargo'


def get_new_command(command, settings):
    return 'cargo build'
