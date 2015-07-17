from thefuck import utils, shells


@utils.git_support
def match(command, settings):
    # catches "git branch list" in place of "git branch"
    return command.script.split() == 'git branch list'.split()


@utils.git_support
def get_new_command(command, settings):
    return shells.and_('git branch --delete list', 'git branch')
