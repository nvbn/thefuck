from mock import patch, Mock
from thefuck.main import Rule
from thefuck import conf


def test_rules_list():
    assert conf.RulesList(['bash', 'lisp']) == ['bash', 'lisp']
    assert conf.RulesList(['bash', 'lisp']) == conf.RulesList(['bash', 'lisp'])
    assert Rule('lisp', None, None, False) in conf.RulesList(['lisp'])
    assert Rule('bash', None, None, False) not in conf.RulesList(['lisp'])


def test_default():
    assert Rule('test', None, None, True) in conf.DEFAULT
    assert Rule('test', None, None, False) not in conf.DEFAULT
    assert Rule('test', None, None, False) in (conf.DEFAULT + ['test'])


def test_settings_defaults():
    with patch('thefuck.conf.load_source', return_value=object()), \
         patch('thefuck.conf.os.environ', new_callable=lambda: {}):
        for key, val in conf.DEFAULT_SETTINGS.items():
            assert getattr(conf.get_settings(Mock()), key) == val


def test_settings_from_file():
    with patch('thefuck.conf.load_source', return_value=Mock(rules=['test'],
                                                             wait_command=10,
                                                             require_confirmation=True,
                                                             no_colors=True)), \
         patch('thefuck.conf.os.environ', new_callable=lambda: {}):
        settings = conf.get_settings(Mock())
        assert settings.rules == ['test']
        assert settings.wait_command == 10
        assert settings.require_confirmation is True
        assert settings.no_colors is True


def test_settings_from_file_with_DEFAULT():
    with patch('thefuck.conf.load_source', return_value=Mock(rules=conf.DEFAULT + ['test'],
                                                             wait_command=10,
                                                             require_confirmation=True,
                                                             no_colors=True)), \
         patch('thefuck.conf.os.environ', new_callable=lambda: {}):
        settings = conf.get_settings(Mock())
        assert settings.rules == conf.DEFAULT + ['test']


def test_settings_from_env():
    with patch('thefuck.conf.load_source', return_value=Mock(rules=['test'],
                                                             wait_command=10)), \
         patch('thefuck.conf.os.environ',
               new_callable=lambda: {'THEFUCK_RULES': 'bash:lisp',
                                     'THEFUCK_WAIT_COMMAND': '55',
                                     'THEFUCK_REQUIRE_CONFIRMATION': 'true',
                                     'THEFUCK_NO_COLORS': 'false'}):
        settings = conf.get_settings(Mock())
        assert settings.rules == ['bash', 'lisp']
        assert settings.wait_command == 55
        assert settings.require_confirmation is True
        assert settings.no_colors is False


def test_settings_from_env_with_DEFAULT():
    with patch('thefuck.conf.load_source', return_value=Mock()), \
         patch('thefuck.conf.os.environ', new_callable=lambda: {'THEFUCK_RULES': 'DEFAULT:bash:lisp'}):
        settings = conf.get_settings(Mock())
        assert settings.rules == conf.DEFAULT + ['bash', 'lisp']


def test_update_settings():
    settings = conf.Settings({'key': 'val'})
    new_settings = settings.update(key='new-val')
    assert new_settings.key == 'new-val'
    assert settings.key == 'val'
