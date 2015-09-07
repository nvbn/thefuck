# Appends .py when executing python files
#
# Example:
# > python foo
# error: python: can't open file 'foo': [Errno 2] No such file or directory
from thefuck.utils import for_app


@for_app('python')
def match(command):
    return not command.script.endswith('.py')


def get_new_command(command):
    return command.script + '.py'
