from mock import Mock
from thefuck.rules.cd_mkdir import match, get_new_command


def test_match():
    assert match(Mock(script='cd foo', stderr='cd: foo: No such file or directory'),
                 None)
    assert match(Mock(script='cd foo/bar/baz', stderr='cd: foo: No such file or directory'),
                 None)
    assert match(Mock(script='cd foo/bar/baz', stderr='cd: can\'t cd to foo/bar/baz'),
                 None)
    assert not match(Mock(script='cd foo',
                          stderr=''), None)
    assert not match(Mock(script='', stderr=''), None)


def test_get_new_command():
    assert get_new_command(Mock(script='cd foo'), None) == 'mkdir -p foo && cd foo'
    assert get_new_command(Mock(script='cd foo/bar/baz'), None) == 'mkdir -p foo/bar/baz && cd foo/bar/baz'
