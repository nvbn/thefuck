from thefuck.utils import for_app


@for_app('rvm', at_least=2)
def match(command):
    args = command.script_parts
    pattern = """RVM is not a function, selecting rubies with 'rvm use ...' will not work.

You need to change your terminal emulator preferences to allow login shell.
Sometimes it is required to use `/bin/bash --login` as the command.
Please visit https://rvm.io/integration/gnome-terminal/ for an example."""

    return args[1] == 'use' and pattern in command.output


def get_new_command(command):
    args = command.script_parts
    return f'rvm install \"ruby-{args[2]}\"; rvm use {args[2]}'
