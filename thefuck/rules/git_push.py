def match(command, settings):
    is_git = ('git' in command.script and 'push' in command.script) or \
              'gp' in command.script
    return (is_git and 'set-upstream' in command.stderr)


def get_new_command(command, settings):
    return command.stderr.split('\n')[-3].strip()
