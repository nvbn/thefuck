import difflib
import os
import re
from subprocess import check_output

import thefuck.logs

# Formulars are base on each local system's status
brew_formulas = []
try:
    brew_path_prefix = check_output(['brew', '--prefix']).strip()
    brew_formula_path = brew_path_prefix + '/Library/Formula'

    for file_name in os.listdir(brew_formula_path):
        if file_name.endswith('.rb'):
            brew_formulas.append(file_name.replace('.rb', ''))
except:
    pass


def _get_similar_formulars(formula_name):
    return difflib.get_close_matches(formula_name, brew_formulas, 1, 0.85)


def match(command, settings):
    is_proper_command = ('brew install' in command.script and
                         'No available formula' in command.stderr)

    has_possible_formulas = False
    if is_proper_command:
        formula = re.findall(r'Error: No available formula for ([a-z]+)',
                             command.stderr)[0]
        has_possible_formulas = len(_get_similar_formulars(formula)) > 0

    return has_possible_formulas


def get_new_command(command, settings):
    not_exist_formula = re.findall(r'Error: No available formula for ([a-z]+)',
                                   command.stderr)[0]
    exist_formula = _get_similar_formulars(not_exist_formula)[0]

    return command.script.replace(not_exist_formula, exist_formula, 1)
