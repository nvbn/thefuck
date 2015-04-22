from mock import Mock
from thefuck.rules.rm_root import match, get_new_command


def test_match():
    assert match(Mock(script='rm -rf /',
                      stderr='add --no-preserve-root'), None)
    assert not match(Mock(script='ls',
                          stderr='add --no-preserve-root'), None)
    assert not match(Mock(script='rm --no-preserve-root /',
                          stderr='add --no-preserve-root'), None)
    assert not match(Mock(script='rm -rf /',
                          stderr=''), None)


def test_get_new_command():
    assert get_new_command(Mock(script='rm -rf /'), None) \
        == 'rm -rf / --no-preserve-root'
