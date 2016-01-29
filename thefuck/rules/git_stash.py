from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    # catches "Please commit or stash them" and "Please, commit your changes or
    # stash them before you can switch branches."
    return 'or stash them' in command.stderr


@git_support
def get_new_command(command):
    formatme = shell.and_('git stash', '{}')
    return formatme.format(command.script)
