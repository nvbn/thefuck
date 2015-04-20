import pytest
from thefuck.main import Command
from thefuck.rules.git_not_command import match, get_new_command


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
def git_command():
    return "* master"


def test_match(git_not_command, git_command, git_not_command_one_of_this):
    assert match(Command('git brnch', '', git_not_command), None)
    assert match(Command('git st', '', git_not_command_one_of_this), None)
    assert not match(Command('ls brnch', '', git_not_command), None)
    assert not match(Command('git branch', '', git_command), None)


def test_get_new_command(git_not_command, git_not_command_one_of_this):
    assert get_new_command(Command('git brnch', '', git_not_command), None)\
        == 'git branch'
    assert get_new_command(
        Command('git st', '', git_not_command_one_of_this), None) == 'git status'
