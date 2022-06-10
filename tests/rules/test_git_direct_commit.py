import pytest

from thefuck.rules.git_direct_commit import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize(
    "script, output",
    [('''git commit -m "make an other commit"''', "Changes not staged for commit")]
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output",
    [('''git commit -m "make a commit"''', "")]
)
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [("git commit -m 'make a commit'", "Untracked files", "git add --all && git commit -m 'make a commit'")]
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
