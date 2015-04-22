import re


def match(command, settings):
    return ('git' in command.script
            and " is not a git command. See 'git --help'." in command.stderr
            and 'Did you mean' in command.stderr)


def get_new_command(command, settings):
    broken_cmd = re.findall(r"git: '([^']*)' is not a git command",
                            command.stderr)[0]
    new_cmd = re.findall(r'Did you mean[^\n]*\n\s*([^\n]*)',
                         command.stderr)[0]
    return command.script.replace(broken_cmd, new_cmd, 1)

