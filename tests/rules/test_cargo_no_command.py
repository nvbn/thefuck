import pytest
from thefuck.rules.cargo_no_command import match, get_new_command
from thefuck.types import Command


no_such_subcommand_old = """No such subcommand

        Did you mean `build`?
"""

no_such_subcommand = """error: no such subcommand

\tDid you mean `build`?
"""


@pytest.mark.parametrize('command', [
    Command('cargo buid', no_such_subcommand_old),
    Command('cargo buils', no_such_subcommand)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('cargo buid', no_such_subcommand_old), 'cargo build'),
    (Command('cargo buils', no_such_subcommand), 'cargo build')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
