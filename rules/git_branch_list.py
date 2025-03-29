from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    # catches "git branch list" in place of "git branch"
    return (command.script_parts
            and command.script_parts[1:] == 'branch list'.split())


@git_support
def get_new_command(command):
    return shell.and_('git branch --delete list', 'git branch')
