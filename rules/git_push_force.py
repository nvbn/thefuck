from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('push' in command.script
            and '! [rejected]' in command.output
            and 'failed to push some refs to' in command.output
            and 'Updates were rejected because the tip of your current branch is behind' in command.output)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'push', 'push --force-with-lease')


enabled_by_default = False
