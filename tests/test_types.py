from thefuck.types import RulesNamesList, Settings
from tests.utils import Rule


def test_rules_names_list():
    assert RulesNamesList(['bash', 'lisp']) == ['bash', 'lisp']
    assert RulesNamesList(['bash', 'lisp']) == RulesNamesList(['bash', 'lisp'])
    assert Rule('lisp') in RulesNamesList(['lisp'])
    assert Rule('bash') not in RulesNamesList(['lisp'])


def test_update_settings():
    settings = Settings({'key': 'val'})
    new_settings = settings.update(key='new-val', unset='unset-value')
    assert new_settings.key == 'val'
    assert new_settings.unset == 'unset-value'
    assert settings.key == 'val'
