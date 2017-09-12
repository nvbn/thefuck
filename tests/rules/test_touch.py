import pytest
from thefuck.rules.touch import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return "touch: cannot touch '/a/b/c':" \
           " No such file or directory"


def test_match(output):
    command = Command('touch /a/b/c', output)
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('touch /a/b/c', ''),
    Command('ls /a/b/c', output())])
def test_not_match(command):
    assert not match(command)


def test_get_new_command(output):
    command = Command('touch /a/b/c', output)
    fixed_command = get_new_command(command)
    assert fixed_command == 'mkdir -p /a/b && touch /a/b/c'
