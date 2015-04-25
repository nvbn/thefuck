import six
from mock import patch, Mock
from thefuck import conf
from tests.utils import Rule


def test_default():
    assert Rule('test', enabled_by_default=True) in conf.DEFAULT_RULES
    assert Rule('test', enabled_by_default=False) not in conf.DEFAULT_RULES
    assert Rule('test', enabled_by_default=False) in (conf.DEFAULT_RULES + ['test'])


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
    with patch('thefuck.conf.load_source', return_value=Mock(rules=conf.DEFAULT_RULES + ['test'],
                                                             wait_command=10,
                                                             require_confirmation=True,
                                                             no_colors=True)), \
         patch('thefuck.conf.os.environ', new_callable=lambda: {}):
        settings = conf.get_settings(Mock())
        assert settings.rules == conf.DEFAULT_RULES + ['test']


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
         patch('thefuck.conf.os.environ', new_callable=lambda: {'THEFUCK_RULES': 'DEFAULT_RULES:bash:lisp'}):
        settings = conf.get_settings(Mock())
        assert settings.rules == conf.DEFAULT_RULES + ['bash', 'lisp']


def test_initialize_settings_file_ignore_if_exists():
    settings_path_mock = Mock(is_file=Mock(return_value=True), open=Mock())
    user_dir_mock = Mock(joinpath=Mock(return_value=settings_path_mock))
    conf.initialize_settings_file(user_dir_mock)
    assert settings_path_mock.is_file.call_count == 1
    assert not settings_path_mock.open.called


def test_initialize_settings_file_create_if_exists_not():
    settings_file = six.StringIO()
    settings_path_mock = Mock(
        is_file=Mock(return_value=False),
        open=Mock(return_value=Mock(
            __exit__=lambda *args: None, __enter__=lambda *args: settings_file
        )),
    )
    user_dir_mock = Mock(joinpath=Mock(return_value=settings_path_mock))
    conf.initialize_settings_file(user_dir_mock)
    settings_file_contents = settings_file.getvalue()
    assert settings_path_mock.is_file.call_count == 1
    assert settings_path_mock.open.call_count == 1
    assert conf.SETTINGS_HEADER in settings_file_contents
    for setting in conf.DEFAULT_SETTINGS.items():
        assert '# {} = {}\n'.format(*setting) in settings_file_contents
    settings_file.close()
