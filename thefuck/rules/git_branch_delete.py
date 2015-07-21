from thefuck import utils


@utils.git_support
def match(command, settings):
    return ('branch -d' in command.script
            and 'If you are sure you want to delete it' in command.stderr)


@utils.git_support
def get_new_command(command, settings):
    return command.script.replace('-d', '-D')
