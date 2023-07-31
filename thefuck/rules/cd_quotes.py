def match(command):
    return command.script_parts[0] == "cd" and command.script.count(" ") > 1 and (not("\"" in command.script))


def get_new_command(command):
    return 'cd \"{}\"'.format(' '.join(command.script_parts[1:]))

enabled_by_default = True
priority = 900  
requires_output = False
