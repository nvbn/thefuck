import re
from thefuck import shells
from thefuck.utils import sudo_support


@sudo_support
def match(command, settings):
    return (command.script.startswith('cd ')
        and ('no such file or directory' in command.stderr.lower()
            or 'cd: can\'t cd to' in command.stderr.lower()))


@sudo_support
def get_new_command(command, settings):
    repl = shells.and_('mkdir -p \\1', 'cd \\1')
    return re.sub(r'^cd (.*)', repl, command.script)
