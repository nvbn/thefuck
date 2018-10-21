import pytest
from thefuck.types import Command
from thefuck.rules.chmod_x import match, get_new_command


@pytest.mark.parametrize('command', [
    Command('حصی', 'command not found: حصی'),
    Command('مس -مش', 'command not found: مس'),
    Command('لهف سفشفعس', 'command not found: لهف'),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('حصی', ''), 'pwd'),
    (Command('مس -مش', ''), 'ls -la'),
    (Command('لهف سفشفعس', ''), 'git status'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
