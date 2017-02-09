import re

from thefuck.utils import for_app, replace_command

no_command = "Error: No such command"
no_website = "hostscli.errors.WebsiteImportError"


@for_app("hostscli")
def match(command):
    errors = [no_command, no_website]
    for error in errors:
        if error in command.stderr:
            return True
    return False


def get_new_command(command):
    if no_website in command.stderr:
        return ['hostscli websites']
    misspelled_command = re.findall(
        r'Error: No such command "(.*)"', command.stderr)[0]
    commands = ['block', 'unblock', 'websites', 'block_all', 'unblock_all']
    return replace_command(command, misspelled_command, commands)
