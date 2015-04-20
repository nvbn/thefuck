from mock import Mock, patch
from thefuck.rules. has_exists_script import match, get_new_command


def test_match():
    with patch('os.path.exists', return_value=True):
        assert match(Mock(script='main', stderr='main: command not found'),
                     None)
        assert match(Mock(script='main --help',
                          stderr='main: command not found'),
                     None)
        assert not match(Mock(script='main', stderr=''), None)

    with patch('os.path.exists', return_value=False):
        assert not match(Mock(script='main', stderr='main: command not found'),
                         None)


def test_get_new_command():
    assert get_new_command(Mock(script='main --help'), None) == './main --help'
