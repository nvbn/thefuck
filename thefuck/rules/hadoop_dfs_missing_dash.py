def match(command, settings):
    return ('hdfs dfs' in command.script
            and "this command begins with a dash." in command.stderr.lower())


def get_new_command(command, settings):
    data = command.script.split()
    data[2] = '-' + data[2]
    return ' '.join(data)

