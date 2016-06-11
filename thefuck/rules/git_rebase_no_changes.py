from thefuck.specific.git import git_support


#@git_support
def match(command):
    return (command.script == 'git rebase --continue' and
            'No changes - did you forget to use \'git add\'?' in command.stdout)


def get_new_command(command):
    return 'git rebase --skip'


enabled_by_default = True
requires_output = True
