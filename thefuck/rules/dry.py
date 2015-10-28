def match(command):
    split_command = command.script_parts

    return (split_command
            and len(split_command) >= 2
            and split_command[0] == split_command[1])


def get_new_command(command):
    return ' '.join(command.script_parts[1:])

# it should be rare enough to actually have to type twice the same word, so
# this rule can have a higher priority to come before things like "cd cd foo"
priority = 900
