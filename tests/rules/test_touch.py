import pytest
from thefuck.rules.touch import match, get_new_command
from thefuck.types import Command


def output(is_bsd):
    if is_bsd:
        return "touch: /a/b/c: No such file or directory"
    return "touch: cannot touch '/a/b/c': No such file or directory"


@pytest.mark.parametrize('script, is_bsd', [
    ('touch /a/b/c', False),
    ('touch /a/b/c', True)])
def test_match(script, is_bsd):
    command = Command(script, output(is_bsd))
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('touch /a/b/c', ''),
    Command('ls /a/b/c', output(False))])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('script, is_bsd', [
    ('touch /a/b/c', False),
    ('touch /a/b/c', True)])
def test_get_new_command(script, is_bsd):
    command = Command(script, output(is_bsd))
    fixed_command = get_new_command(command)
    assert fixed_command == 'mkdir -p /a/b && touch /a/b/c'
