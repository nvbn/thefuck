import pytest
from thefuck.rules.apt_get_search import get_new_command, match
from thefuck.types import Command


def test_match():
    assert match(Command('apt-get search foo', ''))


@pytest.mark.parametrize('command', [
    Command('apt-cache search foo', ''),
    Command('aptitude search foo', ''),
    Command('apt search foo', ''),
    Command('apt-get install foo', ''),
    Command('apt-get source foo', ''),
    Command('apt-get clean', ''),
    Command('apt-get remove', ''),
    Command('apt-get update', '')
])
def test_not_match(command):
    assert not match(command)


def test_get_new_command():
    new_command = get_new_command(Command('apt-get search foo', ''))
    assert new_command == 'apt-cache search foo'
