from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    return 'pull' in command.script and 'set-upstream' in command.output


@git_support
def get_new_command(command):
    line = command.output.split('\n')[-3].strip()
    branch = line.split(' ')[-1]
    set_upstream = line.replace('<remote>', 'origin')\
                       .replace('<branch>', branch)
    return shell.and_(set_upstream, command.script)
