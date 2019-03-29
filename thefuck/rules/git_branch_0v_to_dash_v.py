from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    return (command.script_parts
            and command.script_parts[1:] == 'branch 0v'.split())


@git_support
def get_new_command(command):
    return shell.and_('git branch -D 0v', 'git branch -v')
