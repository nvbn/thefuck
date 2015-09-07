import pytest
from thefuck.rules.cargo_no_command import match, get_new_command
from tests.utils import Command


no_such_subcommand = """No such subcommand

        Did you mean `build`?
"""


@pytest.mark.parametrize('command', [
    Command(script='cargo buid', stderr=no_such_subcommand)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('cargo buid', stderr=no_such_subcommand), 'cargo build')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
