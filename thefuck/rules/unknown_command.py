import re
from thefuck.utils import replace_command


def match(command):
    return (re.search(r"([^:]*): Unknown command.*", command.stderr) != None
            and re.search(r"Did you mean ([^?]*)?", command.stderr) != None)


def get_new_command(command):
    broken_cmd = re.findall(r"([^:]*): Unknown command.*", command.stderr)[0]
    matched = re.findall(r"Did you mean ([^?]*)?", command.stderr)
    return replace_command(command, broken_cmd, matched)
