def match(command, settings):
    return ('git branch -d' in command.script
            and 'If you are sure you want to delete it' in command.stderr)


def get_new_command(command, settings):
    return command.script.replace('-d', '-D')
