from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    '''
    Match a mistyped command
    '''
    return 'lfs' in command.script and 'Did you mean this?' in command.output


@git_support
def get_new_command(command):
    new = command.script.split(' ')
    recommended = command.output.split('\n')[4].strip()
    new[2] = recommended
    return shell.and_(' '.join(new))
