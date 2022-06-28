from thefuck.utils import for_app


@for_app('brew', at_least=2)
def match(command):
    return ('update' in command.script
            and "Error: This command updates brew itself" in command.output
            and "Use `brew upgrade" in command.output)


def get_new_command(command):
    return command.script.replace('update', 'upgrade')
