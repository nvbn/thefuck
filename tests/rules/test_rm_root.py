import pytest
from thefuck.rules.rm_root import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command(script='rm -rf /',
                         stderr='add --no-preserve-root'))


@pytest.mark.parametrize('command', [
    Command(script='ls', stderr='add --no-preserve-root'),
    Command(script='rm --no-preserve-root /', stderr='add --no-preserve-root'),
    Command(script='rm -rf /', stderr='')])
def test_not_match(command):
    assert not match(command)


def test_get_new_command():
    assert get_new_command(Command(script='rm -rf /')) \
           == 'rm -rf / --no-preserve-root'
