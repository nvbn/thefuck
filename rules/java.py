"""Fixes common java command mistake

Example:
> java foo.java
Error: Could not find or load main class foo.java

"""
from thefuck.utils import for_app


@for_app('java')
def match(command):
    return command.script.endswith('.java')


def get_new_command(command):
    return command.script[:-5]
