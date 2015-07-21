from thefuck import utils


@utils.git_support
def match(command, settings):
    return ('push' in command.script
            and 'set-upstream' in command.stderr)


@utils.git_support
def get_new_command(command, settings):
    return command.stderr.split('\n')[-3].strip()
