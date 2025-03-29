import os
import re
from thefuck.utils import get_closest, replace_argument
from thefuck.specific.brew import get_brew_path_prefix, brew_available

enabled_by_default = brew_available


def _get_formulas():
    # Formulas are based on each local system's status
    try:
        brew_path_prefix = get_brew_path_prefix()
        brew_formula_path = brew_path_prefix + '/Library/Formula'

        for file_name in os.listdir(brew_formula_path):
            if file_name.endswith('.rb'):
                yield file_name[:-3]
    except Exception:
        pass


def _get_similar_formula(formula_name):
    return get_closest(formula_name, _get_formulas(), cutoff=0.85)


def match(command):
    is_proper_command = ('brew install' in command.script and
                         'No available formula' in command.output)

    if is_proper_command:
        formula = re.findall(r'Error: No available formula for ([a-z]+)',
                             command.output)[0]
        return bool(_get_similar_formula(formula))
    return False


def get_new_command(command):
    not_exist_formula = re.findall(r'Error: No available formula for ([a-z]+)',
                                   command.output)[0]
    exist_formula = _get_similar_formula(not_exist_formula)

    return replace_argument(command.script, not_exist_formula, exist_formula)
