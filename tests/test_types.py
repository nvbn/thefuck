from thefuck.types import Rule, RulesNamesList, Settings


def test_rules_names_list():
    assert RulesNamesList(['bash', 'lisp']) == ['bash', 'lisp']
    assert RulesNamesList(['bash', 'lisp']) == RulesNamesList(['bash', 'lisp'])
    assert Rule('lisp', None, None, False) in RulesNamesList(['lisp'])
    assert Rule('bash', None, None, False) not in RulesNamesList(['lisp'])


def test_update_settings():
    settings = Settings({'key': 'val'})
    new_settings = settings.update(key='new-val')
    assert new_settings.key == 'new-val'
    assert settings.key == 'val'
