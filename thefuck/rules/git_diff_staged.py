from thefuck import utils


@utils.git_support
def match(command, settings):
    return ('git' in command.script and
            'diff' in command.script and
            '--staged' not in command.script)


@utils.git_support
def get_new_command(command, settings):
    return '{} --staged'.format(command.script)
