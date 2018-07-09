def match(command):
    return (
        command.script.startswith('cat') and
        command.output.startswith('cat: ') and
        command.output.rstrip().endswith(': Is a directory')
    )


def get_new_command(command):
    return command.script.replace('cat', 'ls', 1)
