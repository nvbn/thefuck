import pytest
from thefuck.rules.rm_root import match, get_new_command
from thefuck.types import Command


def test_match():
    assert match(Command('rm -rf /', ''))


@pytest.mark.parametrize('command', [
    Command('ls', 'add --no-preserve-root'),
    Command('rm', '/usr/bin/python')])
def test_not_match(command):
    assert not match(command)


def test_get_new_command():
    assert 'rm' not in (get_new_command(Command('rm -rf /', '')))
