from thefuck.shells import shell
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('push' in command.script and
            '! [rejected]' in command.stderr and
            'failed to push some refs to' in command.stderr and
            ('Updates were rejected because the tip of your'
             ' current branch is behind' in command.stderr or
             'Updates were rejected because the remote '
             'contains work that you do' in command.stderr))


@git_support
def get_new_command(command):
    return shell.and_(replace_argument(command.script, 'push', 'pull'),
                      command.script)
