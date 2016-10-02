from thefuck.utils import for_app


@for_app('brew', at_least=2)
def match(command):
    return (command.script_parts[1] in ['ln', 'link']
            and "brew link --overwrite --dry-run" in command.stderr)


def get_new_command(command):
    command.script_parts[1] = 'link'
    command.script_parts.insert(2, '--overwrite')
    command.script_parts.insert(3, '--dry-run')
    return ' '.join(command.script_parts)
