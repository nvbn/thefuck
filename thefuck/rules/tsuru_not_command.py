import re
from thefuck.utils import (get_closest, replace_argument,
                           get_all_matched_commands, replace_command)


def match(command, settings):
    return (command.script.startswith('tsuru ')
            and ' is not a tsuru command. See "tsuru help".' in command.stderr
            and '\nDid you mean?\n\t' in command.stderr)


def get_new_command(command, settings):
    broken_cmd = re.findall(r'tsuru: "([^"]*)" is not a tsuru command',
                            command.stderr)[0]
    return replace_command(command, broken_cmd,
                           get_all_matched_commands(command.stderr))

