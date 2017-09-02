import pytest
from thefuck.rules.git_stash_pop import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return '''error: Your local changes to the following files would be overwritten by merge:'''


def test_match(output):
    assert match(Command('git stash pop', output))
    assert not match(Command('git stash', ''))


def test_get_new_command(output):
    assert (get_new_command(Command('git stash pop', output))
            == "git add --update && git stash pop && git reset .")
