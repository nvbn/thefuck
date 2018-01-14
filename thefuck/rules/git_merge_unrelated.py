from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('merge' in command.script
            and 'fatal: refusing to merge unrelated histories' in command.output)


@git_support
def get_new_command(command):
    return command.script + ' --allow-unrelated-histories'
