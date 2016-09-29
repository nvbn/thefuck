from thefuck.utils import for_app


@for_app('brew', at_least=2)
def match(command):
    return (command.script_parts[1] in ['uninstall', 'rm', 'remove']
            and "brew uninstall --force" in command.stdout)


def get_new_command(command):
    command.script_parts[1] = 'uninstall'
    command.script_parts.insert(2, '--force')
    return ' '.join(command.script_parts)
