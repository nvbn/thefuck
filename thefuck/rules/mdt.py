import re
from thefuck.shells import shell
from thefuck.utils import for_app
from thefuck.utils import which


@for_app('mdt')
def match(command):
    return "Unknown command" in command.output and "try 'mdt help'" in command.output


def get_new_command(command):
    corrections = ["help"]
    command = str(command)
    extracted_command = re.findall(r"'(.*?)'", command)[0]

    if re.match('[shell]{2,}', extracted_command):
        corrections.insert(0, "shell")

    return ["mdt " + correction for correction in corrections]
