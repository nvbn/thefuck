import pytest
from thefuck.rules.git_add import match, get_new_command
from tests.utils import Command


@pytest.fixture
def did_not_match(target, did_you_forget=True):
    error = ("error: pathspec '{}' did not match any "
             "file(s) known to git.".format(target))
    if did_you_forget:
        error = ("{}\nDid you forget to 'git add'?'".format(error))
    return error


@pytest.mark.parametrize('command', [
    Command(script='git submodule update unknown',
            stderr=did_not_match('unknown')),
    Command(script='git commit unknown',
            stderr=did_not_match('unknown'))])  # Older versions of Git
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='git submodule update known', stderr=('')),
    Command(script='git commit known', stderr=('')),
    Command(script='git commit unknown',  # Newer versions of Git
            stderr=did_not_match('unknown', False))])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('git submodule update unknown', stderr=did_not_match('unknown')),
     'git add -- unknown && git submodule update unknown'),
    (Command('git commit unknown', stderr=did_not_match('unknown')),  # Old Git
     'git add -- unknown && git commit unknown')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
