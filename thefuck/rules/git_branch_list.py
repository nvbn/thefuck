from thefuck import shells


def match(command, settings):
    # catches "git branch list" in place of "git branch"
    return command.script.split() == 'git branch list'.split()


def get_new_command(command, settings):
    return shells.and_('git branch --delete list', 'git branch')
