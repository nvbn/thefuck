def match(command, settings):
    return (('g++' in command.script or 'clang++' in command.script) and
            ('This file requires compiler and library support for the '
             'ISO C++ 2011 standard.' in command.stderr or
             '-Wc++11-extensions' in command.stderr))


def get_new_command(command, settings):
    return command.script + ' -std=c++11'
