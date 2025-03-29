from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('pull' in command.script
            and ('You have unstaged changes' in command.output
                 or 'contains uncommitted changes' in command.output))


@git_support
def get_new_command(command):
    return shell.and_('git stash', 'git pull', 'git stash pop')
