# Appends .java when compiling java files
#
# Example:
# > javac foo
# error: Class names, 'foo', are only accepted if annotation
# processing is explicitly requested


def match(command, settings):
    return (command.script.startswith('javac ')
            and not command.script.endswith('.java'))


def get_new_command(command, settings):
    return command.script + '.java'
