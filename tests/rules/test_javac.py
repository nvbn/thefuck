import pytest
from thefuck.rules.javac import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('javac foo', ''),
    Command('javac bar', '')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('javac foo', ''), 'javac foo.java'),
    (Command('javac bar', ''), 'javac bar.java')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
