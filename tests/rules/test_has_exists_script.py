from mock import patch
from thefuck.rules.has_exists_script import match, get_new_command
from ..utils import Command


def test_match():
    with patch('os.path.exists', return_value=True):
        assert match(Command(script='main', stderr='main: command not found'))
        assert match(Command(script='main --help',
                          stderr='main: command not found'))
        assert not match(Command(script='main', stderr=''))

    with patch('os.path.exists', return_value=False):
        assert not match(Command(script='main', stderr='main: command not found'))


def test_get_new_command():
    assert get_new_command(Command(script='main --help')) == './main --help'
