import pytest

from thefuck.rules.rm_root import get_new_command, match
from thefuck.types import Command


def test_match():
    assert match(Command('rm -rf /', 'add --no-preserve-root'))


@pytest.mark.parametrize('command', [
    Command('ls', 'add --no-preserve-root'),
    Command('rm --no-preserve-root /', 'add --no-preserve-root'),
    Command('rm -rf /', '')])
def test_not_match(command):
    assert not match(command)


def test_get_new_command():
    assert (get_new_command(Command('rm -rf /', ''))
            == 'rm -rf / --no-preserve-root')
