import re
from thefuck.utils import get_all_matched_commands, replace_command, for_app


@for_app('tsuru')
def match(command):
    return (' is not a tsuru command. See "tsuru help".' in command.output
            and '\nDid you mean?\n\t' in command.output)


def get_new_command(command):
    broken_cmd = re.findall(r'tsuru: "([^"]*)" is not a tsuru command',
                            command.output)[0]
    return replace_command(command, broken_cmd,
                           get_all_matched_commands(command.output))
