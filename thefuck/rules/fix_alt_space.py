# -*- encoding: utf-8 -*-

import re
from thefuck.utils import sudo_support


@sudo_support
def match(command, settings):
    return ('command not found' in command.stderr.lower()
            and u' ' in command.script)


@sudo_support
def get_new_command(command, settings):
    return re.sub(u' ', ' ', command.script)
