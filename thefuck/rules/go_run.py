# Appends .go when compiling go files
#
# Example:
# > go run foo
# error: go run: no go files listed


def match(command, settings):
    return (command.script.startswith('go run ')
            and not command.script.endswith('.go'))


def get_new_command(command, settings):
    return command.script + '.go'
