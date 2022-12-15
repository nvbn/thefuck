from thefuck.shells import shell
from thefuck.utils import for_app


@for_app('terraform')
def match(command):
    return 'Inconsistent dependency lock file' in command.output
           
def get_new_command(command):
    return shell.and_('terraform init -upgrade', command.script)
