from thefuck.utils import replace_argument


def match(command):
    return "php -s" in command.script


def get_new_command(command):
    return replace_argument(command.script, "-s", "-S")
