import re
from thefuck.utils import for_app, replace_argument
from thefuck.specific.brew import brew_available

enabled_by_default = brew_available


@for_app('brew', at_least=2)
def match(command):
    is_proper_command = ('install' in command.script and
                         'No available formula' in command.output and
                         'Did you mean' in command.output)
    return is_proper_command


def get_new_command(command):
    matcher = re.search('Warning: No available formula with the name "([^"]+)". Did you mean ([^, ?]+)',
                         command.output)
    not_exist_formula = matcher.group(1)
    exist_formula = matcher.group(2)
    return replace_argument(command.script, not_exist_formula, exist_formula)
