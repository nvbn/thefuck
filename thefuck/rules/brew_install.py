import os
import re
from subprocess import check_output
from thefuck.utils import get_closest

# Formulars are base on each local system's status

brew_formulas = []
try:
    brew_path_prefix = check_output(['brew', '--prefix'],
                                    universal_newlines=True).strip()
    brew_formula_path = brew_path_prefix + '/Library/Formula'

    for file_name in os.listdir(brew_formula_path):
        if file_name.endswith('.rb'):
            brew_formulas.append(file_name.replace('.rb', ''))
except:
    pass


def _get_similar_formula(formula_name):
    return get_closest(formula_name, brew_formulas, 1, 0.85)


def match(command, settings):
    is_proper_command = ('brew install' in command.script and
                         'No available formula' in command.stderr)

    has_possible_formulas = False
    if is_proper_command:
        formula = re.findall(r'Error: No available formula for ([a-z]+)',
                             command.stderr)[0]
        has_possible_formulas = bool(_get_similar_formula(formula))

    return has_possible_formulas


def get_new_command(command, settings):
    not_exist_formula = re.findall(r'Error: No available formula for ([a-z]+)',
                                   command.stderr)[0]
    exist_formula = _get_similar_formula(not_exist_formula)

    return command.script.replace(not_exist_formula, exist_formula, 1)
