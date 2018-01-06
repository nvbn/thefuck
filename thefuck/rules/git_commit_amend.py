from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('commit' in command.script_parts)


@git_support
def get_new_command(command):
    return 'git commit --amend'
