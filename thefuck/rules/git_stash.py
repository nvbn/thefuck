from thefuck import shells, utils
from thefuck.specific.git import git_support


@git_support
def match(command, settings):
    # catches "Please commit or stash them" and "Please, commit your changes or
    # stash them before you can switch branches."
    return 'or stash them' in command.stderr


@git_support
def get_new_command(command, settings):
    formatme = shells.and_('git stash', '{}')
    return formatme.format(command.script)
