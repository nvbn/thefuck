import pytest
from thefuck.rules.git_flag_after_filename import match, get_new_command
from tests.utils import Command

command1 = Command('git log README.md -p',
                   stderr="fatal: bad flag '-p' used after filename")
command2 = Command('git log README.md -p CONTRIBUTING.md',
                   stderr="fatal: bad flag '-p' used after filename")
command3 = Command('git log -p README.md --name-only',
                   stderr="fatal: bad flag '--name-only' used after filename")


@pytest.mark.parametrize('command', [
    command1, command2, command3])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('git log README.md'),
    Command('git log -p README.md')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, result', [
    (command1, "git log -p README.md"),
    (command2, "git log -p README.md CONTRIBUTING.md"),
    (command3, "git log -p --name-only README.md")])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
