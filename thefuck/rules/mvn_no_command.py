from thefuck import shells

def match(command, settings):
    return 'No goals have been specified for this build' in command.stdout and command.script.startswith('mvn')


def get_new_command(command, settings):
    return [ command.script + ' clean package', command.script + ' clean install']
