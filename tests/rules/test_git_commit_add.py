import pytest
from thefuck.rules.git_commit_add import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize(
    "script, output",
    [
        ('git commit -m "test"', "no changes added to commit"),
        ("git commit", "no changes added to commit"),
    ],
)
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output",
    [
        ('git commit -m "test"', " 1 file changed, 15 insertions(+), 14 deletions(-)"),
        ("git branch foo", ""),
        ("git checkout feature/test_commit", ""),
        ("git push", ""),
    ],
)
def test_not_match(output, script):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, new_command",
    [
        ("git commit", ["git commit -a", "git commit -p"]),
        ('git commit -m "foo"', ['git commit -a -m "foo"', 'git commit -p -m "foo"']),
    ],
)
def test_get_new_command(script, new_command):
    assert get_new_command(Command(script, "")) == new_command
