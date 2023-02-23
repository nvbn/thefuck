#
# $ poetry updat
#
# The command "updat" does not exist.
#
# Did you mean one of these?
#     update
#     self update
#
# $ fuck
# poetry update [enter/↑/↓/ctrl+c]
#
import re
from thefuck.utils import for_app

REGEX = r"(?m)(?<=Did you mean one of these\?\n)(\s+(.+)$)+"


@for_app("poetry")
def match(command):
    return """Did you mean one of these?""" in command.output


def get_new_command(command) -> str | list[str]:
    if matches := re.search(REGEX, command.output):
        return [f"poetry {s.strip()}" for s in matches.group().split("\n")]
    else:
        return ""


enabled_by_default = True
