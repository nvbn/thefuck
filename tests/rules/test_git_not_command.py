import pytest
from thefuck.rules.git_not_command import match, get_new_command
from tests.utils import Command


@pytest.fixture
def git_not_command():
    return """git: 'brnch' is not a git command. See 'git --help'.

Did you mean this?
branch
"""


@pytest.fixture
def git_not_command_one_of_this():
    return """git: 'st' is not a git command. See 'git --help'.

Did you mean one of these?
status
reset
stage
stash
stats
"""


@pytest.fixture
def git_not_command_closest():
    return '''git: 'tags' is not a git command. See 'git --help'.

Did you mean one of these?
\tstage
\ttag
'''


@pytest.fixture
def git_command():
    return "* master"


def test_match(git_not_command, git_command, git_not_command_one_of_this):
    assert match(Command('git brnch', stderr=git_not_command), None)
    assert match(Command('git st', stderr=git_not_command_one_of_this), None)
    assert not match(Command('ls brnch', stderr=git_not_command), None)
    assert not match(Command('git branch', stderr=git_command), None)


def test_get_new_command(git_not_command, git_not_command_one_of_this,
                         git_not_command_closest):
    assert get_new_command(Command('git brnch', stderr=git_not_command), None) \
           == ['git branch']
    assert get_new_command(Command('git st', stderr=git_not_command_one_of_this),
                           None) == ['git stats', 'git stash', 'git stage']
    assert get_new_command(Command('git tags', stderr=git_not_command_closest),
                           None) == ['git tag', 'git stage']
