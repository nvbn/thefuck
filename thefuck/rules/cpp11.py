from thefuck.utils import for_app


@for_app('g++', 'clang++')
def match(command):
    return (
        'This file requires compiler and library support for the '
        'ISO C++ 2011 standard.' in command.output or
        '-Wc++11-extensions' in command.output
    )


def get_new_command(command):
    return command.script + ' -std=c++11'
