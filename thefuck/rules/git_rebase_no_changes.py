from thefuck.specific.git import git_support


@git_support
def match(command):
    return (
        {'rebase', '--continue'}.issubset(command.script_parts) and
        'No changes - did you forget to use \'git add\'?' in command.output
    )


def get_new_command(command):
    return 'git rebase --skip'
