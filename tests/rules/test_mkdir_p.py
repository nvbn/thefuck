import pytest
from thefuck.rules.mkdir_p import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('mkdir foo/bar/baz',
                         stderr='mkdir: foo/bar: No such file or directory'),
                 None)


@pytest.mark.parametrize('command', [
    Command('mkdir foo/bar/baz'),
    Command('mkdir foo/bar/baz', stderr='foo bar baz'),
    Command()])
def test_not_match(command):
    assert not match(command, None)


def test_get_new_command():
    assert get_new_command(Command('mkdir foo/bar/baz'), None)\
           == 'mkdir -p foo/bar/baz'
