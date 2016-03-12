from thefuck.specific.git import git_support


@git_support
def match(command):
    return 'help' in command.script and ' is aliased to ' in command.stdout


@git_support
def get_new_command(command):
    aliased = command.stdout.split('`', 2)[2].split("'", 1)[0].split(' ', 1)[0]
    return 'git help {}'.format(aliased)
