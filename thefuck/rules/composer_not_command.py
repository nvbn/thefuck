import re


def match(command, settings):
    return ('composer' in command.script
            and ('did you mean this?' in command.stderr.lower()
                 or 'did you mean one of these?' in command.stderr.lower()))


def get_new_command(command, settings):
    broken_cmd = re.findall(r"Command \"([^']*)\" is not defined", command.stderr)[0]
    new_cmd = re.findall(r'Did you mean this\?[^\n]*\n\s*([^\n]*)', command.stderr)
    if not new_cmd:
        new_cmd = re.findall(r'Did you mean one of these\?[^\n]*\n\s*([^\n]*)', command.stderr)
    return command.script.replace(broken_cmd, new_cmd[0].strip(), 1)