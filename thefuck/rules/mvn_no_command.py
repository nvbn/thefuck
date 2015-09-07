from thefuck.utils import for_app


@for_app('mvn')
def match(command):
    return 'No goals have been specified for this build' in command.stdout


def get_new_command(command):
    return [command.script + ' clean package',
            command.script + ' clean install']
