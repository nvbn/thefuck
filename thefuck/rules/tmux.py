import re


def match(command, settings):
    return ('tmux' in command.script
            and 'ambiguous command:' in command.stderr
            and 'could be:' in command.stderr)


def get_new_command(command, settings):
    cmd = re.match(r"ambiguous command: (.*), could be: ([^, \n]*)",
                   command.stderr)

    return command.script.replace(cmd.group(1), cmd.group(2))
