def match(command, settings):
    return command.script.startswith('man')


def get_new_command(command, settings):
    if '3' in command.script:
        return command.script.replace("3", "2")
    if '2' in command.script:
        return command.script.replace("2", "3")

    split_cmd = command.script.split()
    split_cmd.insert(1, ' 3 ')
    return "".join(split_cmd)
