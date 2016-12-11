import pytest
from thefuck.rules.git_stash_pop import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return '''error: Your local changes to the following files would be overwritten by merge:'''


def test_match(stderr):
    assert match(Command('git stash pop', stderr=stderr))
    assert not match(Command('git stash'))


def test_get_new_command(stderr):
    assert get_new_command(Command('git stash pop', stderr=stderr)) \
           == "git add . && git stash pop && git reset ."
