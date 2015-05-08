def match(command, settings):
    split_command = command.script.split()

    return len(split_command) >= 2 and split_command[0] == split_command[1]


def get_new_command(command, settings):
    return command.script[command.script.find(' ')+1:]

# it should be rare enough to actually have to type twice the same word, so
# this rule can have a higher priority to come before things like "cd cd foo"
priority = 900
