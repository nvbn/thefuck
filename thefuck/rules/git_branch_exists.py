import re
from thefuck.shells import shell
from thefuck.specific.git import git_support
from thefuck.utils import eager


@git_support
def match(command):
    return ("fatal: A branch named '" in command.stderr
            and " already exists." in command.stderr)


@git_support
@eager
def get_new_command(command):
    branch_name = re.findall(
        r"fatal: A branch named '([^']*)' already exists.", command.stderr)[0]
    new_command_templates = [['git branch -d {0}', 'git branch {0}'],
                             ['git branch -d {0}', 'git checkout -b {0}'],
                             ['git branch -D {0}', 'git branch {0}'],
                             ['git branch -D {0}', 'git checkout -b {0}'],
                             ['git checkout {0}']]
    for new_command_template in new_command_templates:
        yield shell.and_(*new_command_template).format(branch_name)
