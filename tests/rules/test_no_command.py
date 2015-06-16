from mock import patch, Mock
from thefuck.rules.no_command import match, get_new_command, _get_all_callables


@patch('thefuck.rules.no_command._safe', return_value=[])
@patch('thefuck.rules.no_command.get_aliases',
       return_value=['vim', 'apt-get', 'fsck', 'fuck'])
def test_get_all_callables(*args):
    all_callables = _get_all_callables()
    assert 'vim' in all_callables
    assert 'fsck' in all_callables
    assert 'fuck' not in all_callables


@patch('thefuck.rules.no_command._safe', return_value=[])
@patch('thefuck.rules.no_command.get_aliases',
       return_value=['vim', 'apt-get', 'fsck', 'fuck'])
def test_match(*args):
    assert match(Mock(stderr='vom: not found', script='vom file.py'), None)
    assert match(Mock(stderr='fucck: not found', script='fucck'), None)
    assert not match(Mock(stderr='qweqwe: not found', script='qweqwe'), None)
    assert not match(Mock(stderr='some text', script='vom file.py'), None)


@patch('thefuck.rules.no_command._safe', return_value=[])
@patch('thefuck.rules.no_command.get_aliases',
       return_value=['vim', 'apt-get', 'fsck', 'fuck'])
def test_get_new_command(*args):
    assert get_new_command(
        Mock(stderr='vom: not found',
             script='vom file.py'),
        None) == 'vim file.py'
    assert get_new_command(
        Mock(stderr='fucck: not found',
             script='fucck'),
        None) == 'fsck'
