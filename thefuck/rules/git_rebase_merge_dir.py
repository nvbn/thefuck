from difflib import get_close_matches
from thefuck.specific.git import git_support


@git_support
def match(command):
    return (' rebase' in command.script and
            'It seems that there is already a rebase-merge directory' in command.stderr and
            'I wonder if you are in the middle of another rebase' in command.stderr)


@git_support
def get_new_command(command):
    command_list = ['git rebase --continue', 'git rebase --abort', 'git rebase --skip']
    rm_cmd = command.stderr.split('\n')[-4]
    command_list.append(rm_cmd.strip())
    return get_close_matches(command.script, command_list, 4, 0)
