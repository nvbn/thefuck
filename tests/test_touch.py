import pytest
from thefuck.rules.touch import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return "touch: cannot touch '/a/b/c':" \
           " No such file or directory"


def test_match(stderr):
    command = Command(
        'touch /a/b/c', stderr=stderr)
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('touch /a/b/c'),
    Command('touch /a/b/c', stdout=stderr()),
    Command('ls /a/b/c', stderr=stderr())])
def test_not_match(command):
    assert not match(command)


def test_get_new_command(stderr):
    command = Command('touch /a/b/c', stderr=stderr)
    fixed_command = get_new_command(command)
    assert fixed_command == 'mkdir -p /a/b && touch /a/b/c'
