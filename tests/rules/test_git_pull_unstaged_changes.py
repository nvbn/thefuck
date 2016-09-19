import pytest
from thefuck.rules.git_pull_uncommitted_changes import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return '''error: Cannot pull with rebase: Your index contains uncommitted changes.'''


def test_match(stderr):
    assert match(Command('git pull', stderr=stderr))
    assert not match(Command('git pull'))
    assert not match(Command('ls', stderr=stderr))


def test_get_new_command(stderr):
    assert get_new_command(Command('git pull', stderr=stderr)) \
           == "git stash && git pull && git stash pop"
