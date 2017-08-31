from thefuck.utils import for_app


@for_app('ls')
def match(command):
    return command.output.strip() == ''


def get_new_command(command):
    return ' '.join(['ls', '-A'] + command.script_parts[1:])
