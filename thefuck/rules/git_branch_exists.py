import re
from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('branch' in command.script
            and "fatal: A branch named '" in command.stderr
            and " already exists." in command.stderr)


@git_support
def get_new_command(command):
    branch_name = re.findall(
        r"fatal: A branch named '([^']*)' already exists.", command.stderr)[0]
    return_ = [shell.and_(*cmd_list).format(branch_name) for cmd_list in [
        ['git branch -d {0}', 'git branch {0}'],
        ['git branch -D {0}', 'git branch {0}'],
        ['git checkout {0}']]]
    return return_
