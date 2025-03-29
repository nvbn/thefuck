import re
from thefuck.utils import replace_argument, for_app


@for_app('composer')
def match(command):
    return (('did you mean this?' in command.output.lower()
             or 'did you mean one of these?' in command.output.lower())) or (
        "install" in command.script_parts and "composer require" in command.output.lower()
    )


def get_new_command(command):
    if "install" in command.script_parts and "composer require" in command.output.lower():
        broken_cmd, new_cmd = "install", "require"
    else:
        broken_cmd = re.findall(r"Command \"([^']*)\" is not defined", command.output)[0]
        new_cmd = re.findall(r'Did you mean this\?[^\n]*\n\s*([^\n]*)', command.output)
        if not new_cmd:
            new_cmd = re.findall(r'Did you mean one of these\?[^\n]*\n\s*([^\n]*)', command.output)
        new_cmd = new_cmd[0].strip()
    return replace_argument(command.script, broken_cmd, new_cmd)
