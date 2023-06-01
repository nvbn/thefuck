import re
from thefuck.utils import for_app


@for_app('mdt')
def match(command):
    return "Unknown command" in command.output and "try 'mdt help'" in command.output


def get_new_command(command):
    corrections = ["help"]

    """ Extract what the user typed in"""
    command = str(command)
    extracted_command = re.findall(r"'(.*?)'", command)[0]

    """ Find possible matches in the case of typos"""
    if re.match('[shell]{2,}', extracted_command):
        corrections.insert(0, "shell")
    elif re.match('[devices]{3,}', extracted_command):
        corrections.insert(0, "devices")
    elif re.match('[reboot]{2,}', extracted_command):
        corrections.insert(0, "reboot")
        corrections.insert(1, "reboot-bootloader")
    elif re.match('[version]{3,}', extracted_command):
        corrections.insert(0, "version")
    elif re.match('[wait\-for\-device]{3,}', extracted_command):
        corrections.insert(0, "wait-for-device")

    return ["mdt " + correction for correction in corrections]
