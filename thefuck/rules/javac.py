"""Appends .java when compiling java files

Example:
 > javac foo
 error: Class names, 'foo', are only accepted if annotation
 processing is explicitly requested

"""
from thefuck.utils import for_app


@for_app('javac')
def match(command, settings):
    return not command.script.endswith('.java')


def get_new_command(command, settings):
    return command.script + '.java'
