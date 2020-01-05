import re
from thefuck.utils import for_app
from thefuck.specific.sudo import sudo_support
from thefuck.shells import shell


@sudo_support
@for_app('cd')
def match(command):
    return (
        command.script.startswith('cd ') and any((
            'no such file or directory' in command.output.lower(),
            'cd: can\'t cd to' in command.output.lower(),
            'does not exist' in command.output.lower()
        )))


@sudo_support
def get_new_command(command):
    repl = shell.and_('mkdir -p \\1', 'cd \\1')
    return re.sub(r'^cd (.*)', repl, command.script)
