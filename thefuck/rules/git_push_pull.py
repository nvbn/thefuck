from thefuck import utils
from thefuck.shells import and_


@utils.git_support
def match(command, settings):
    return ('git' in command.script
            and 'push' in command.script
            and '! [rejected]' in command.stderr
            and 'failed to push some refs to' in command.stderr
            and 'Updates were rejected because the tip of your current branch is behind' in command.stderr)


@utils.git_support
def get_new_command(command, settings):
    return and_(command.script.replace('push', 'pull'),
                command.script)
