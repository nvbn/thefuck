from thefuck.utils import for_app


@for_app('mvn')
def match(command, settings):
    return 'No goals have been specified for this build' in command.stdout


def get_new_command(command, settings):
    return [command.script + ' clean package',
            command.script + ' clean install']
