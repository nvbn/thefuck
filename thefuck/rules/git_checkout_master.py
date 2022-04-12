import subprocess
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ("error: pathspec 'master' did not match any file(s) known to git"
            in command.output
            and "Did you forget to 'git add'?" not in command.output)


def main_branch_exists():
    proc = subprocess.Popen(
        ['git', 'branch', '-a', '--list', 'main'],
        stdout=subprocess.PIPE)
    branches = [i.decode('utf-8').strip() for i in proc.stdout.readlines()]
    return 'remotes/origin/main' in branches


@git_support
def get_new_command(command):
    if main_branch_exists():
        return replace_argument(command.script, 'checkout master', 'checkout main')

    return []
