from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('stash' in command.script
            and 'pop' in command.script
            and 'Your local changes to the following files would be overwritten by merge' in command.output)


@git_support
def get_new_command(command):
    return shell.and_('git add --update', 'git stash pop', 'git reset .')


# make it come before the other applicable rules
priority = 900
