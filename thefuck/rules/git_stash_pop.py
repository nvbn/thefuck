from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('stash' in command.script
            and 'pop' in command.script
            and 'Your local changes to the following files would be overwritten by merge' in command.output)


@git_support
def get_new_command(command):
    cmd = command.script_parts[0]
    return shell.and_('{} add --update'.format(cmd), '{} stash pop'.format(cmd), '{} reset .'.format(cmd))


# make it come before the other applicable rules
priority = 900
