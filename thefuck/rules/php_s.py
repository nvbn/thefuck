from thefuck.utils import replace_argument, for_app


@for_app('php')
def match(command):
    return "php -s" in command.script


def get_new_command(command):
    return replace_argument(command.script, "-s", "-S")


enabled_by_default = True
requires_output = False
