import re
from thefuck.utils import get_all_matched_commands, replace_command


def match(command):
    '''
    Match a mistyped command
    '''
    return 'conda' in command.script and "Did you mean 'conda" in command.output


def get_new_command(command):
    match = re.findall(r"'conda ([^']*)'", command.output)
    broken_cmd = match[0]
    correct_cmd = match[1]
    return replace_command(command, broken_cmd, [correct_cmd])
