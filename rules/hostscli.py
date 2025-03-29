import re
from thefuck.specific.sudo import sudo_support
from thefuck.utils import replace_command, for_app

no_command = "Error: No such command"
no_website = "hostscli.errors.WebsiteImportError"


@sudo_support
@for_app('hostscli')
def match(command):
    errors = [no_command, no_website]
    for error in errors:
        if error in command.output:
            return True
    return False


@sudo_support
def get_new_command(command):
    if no_website in command.output:
        return ['hostscli websites']

    misspelled_command = re.findall(
        r'Error: No such command ".*"', command.output)[0]
    commands = ['block', 'unblock', 'websites', 'block_all', 'unblock_all']
    return replace_command(command, misspelled_command, commands)
