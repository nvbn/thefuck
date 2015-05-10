from mock import patch, Mock
from thefuck.rules.ls_lah import match, get_new_command


def test_match():
    assert match(Mock(script='ls file.py'), None)
    assert match(Mock(script='ls /opt'), None)
    assert not match(Mock(script='ls -lah /opt'), None)


def test_get_new_command():
    assert get_new_command(Mock(script='ls file.py'), None) == 'ls -lah file.py'
    assert get_new_command(Mock(script='ls'), None) == 'ls -lah'
