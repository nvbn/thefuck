import pytest
from thefuck.rules.ag_literal import match, get_new_command
from tests.utils import Command

stderr = ('ERR: Bad regex! pcre_compile() failed at position 1: missing )\n'
          'If you meant to search for a literal string, run ag with -Q\n')

matching_command = Command(script='ag \\(', stderr=stderr)

@pytest.mark.parametrize('command', [
    matching_command])
def test_match(command):
    assert match(matching_command)


@pytest.mark.parametrize('command', [
    Command(script='ag foo', stderr='')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (matching_command, 'ag -Q \\(')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
