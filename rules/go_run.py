from thefuck.utils import for_app
# Appends .go when compiling go files
#
# Example:
# > go run foo
# error: go run: no go files listed


@for_app('go')
def match(command):
    return (command.script.startswith('go run ')
            and not command.script.endswith('.go'))


def get_new_command(command):
    return command.script + '.go'
