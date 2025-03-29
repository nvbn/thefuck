import re
from thefuck.utils import replace_command, get_all_matched_commands, for_app
from thefuck.specific.sudo import sudo_support


@sudo_support
@for_app('lein')
def match(command):
    return (command.script.startswith('lein')
            and "is not a task. See 'lein help'" in command.output
            and 'Did you mean this?' in command.output)


@sudo_support
def get_new_command(command):
    broken_cmd = re.findall(r"'([^']*)' is not a task",
                            command.output)[0]
    new_cmds = get_all_matched_commands(command.output, 'Did you mean this?')
    return replace_command(command, broken_cmd, new_cmds)
