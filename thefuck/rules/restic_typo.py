import re
from thefuck.utils import replace_command, for_app


@for_app("restic")
def match(command):
    return (re.search('unknown command ".*" for "restic"', command.output)
            and "Did you mean this" in command.output)


def get_new_command(command):
    broken_cmd = re.findall(r"(?<=unknown command \")([a-z\-]+)", command.output)[0]
    correct_cmd = re.findall(r"([a-z\-]+)", command.output)[-1]
    return replace_command(command, broken_cmd, [correct_cmd])
