from thefuck.specific.git import git_support


@git_support
def match(command):
    return 'git: \'lock\' is not a git command.' in command.output


@git_support
def get_new_command(command):
    return command.script.replace('lock', 'log', 1)
