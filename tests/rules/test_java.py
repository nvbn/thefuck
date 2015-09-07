import pytest
from thefuck.rules.java import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='java foo.java'),
    Command(script='java bar.java')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('java foo.java'), 'java foo'),
    (Command('java bar.java'), 'java bar')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
