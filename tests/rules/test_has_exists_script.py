from mock import patch
from thefuck.rules.has_exists_script import match, get_new_command
from thefuck.types import Command


def test_match():
    with patch('os.path.exists', return_value=True):
        assert match(Command('main', 'main: command not found'))
        assert match(Command('main --help',
                             'main: command not found'))
        assert not match(Command('main', ''))

    with patch('os.path.exists', return_value=False):
        assert not match(Command('main', 'main: command not found'))


def test_get_new_command():
    assert get_new_command(Command('main --help', '')) == './main --help'
