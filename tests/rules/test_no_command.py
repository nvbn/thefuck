from mock import patch, Mock
from thefuck.rules.no_command import match, get_new_command


def test_match():
    with patch('thefuck.rules.no_command._get_all_callables',
               return_value=['vim', 'apt-get']):
        assert match(Mock(stderr='vom: not found', script='vom file.py'), None)
        assert not match(Mock(stderr='qweqwe: not found', script='qweqwe'), None)
        assert not match(Mock(stderr='some text', script='vom file.py'), None)


def test_get_new_command():
    with patch('thefuck.rules.no_command._get_all_callables',
               return_value=['vim', 'apt-get']):
        assert get_new_command(
            Mock(stderr='vom: not found',
                 script='vom file.py'),
            None) == 'vim file.py'
