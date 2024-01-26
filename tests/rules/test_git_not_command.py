import pytest
from thefuck.rules.git_not_command import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def git_not_command():
    return """git: 'brnch' is not a git command. See 'git --help'.

The most similar command is
branch
"""


@pytest.fixture
def git_not_command_one_of_this():
    return """git: 'st' is not a git command. See 'git --help'.

The most similar commands are
status
reset
stage
stash
stats
"""


@pytest.fixture
def git_not_command_closest():
    return '''git: 'tags' is not a git command. See 'git --help'.

The most similar commands are
\tstage
\ttag
'''


@pytest.fixture
def git_not_command_uncommon():
    return "git: 'lock' is not a git command. See 'git --help'.\n\nThe most similar command is"


@pytest.fixture
def git_command():
    return "* master"


def test_match(git_not_command, git_command, git_not_command_one_of_this, git_not_command_closest, git_not_command_uncommon):
    assert match(Command('git brnch', git_not_command))
    assert match(Command('git st', git_not_command_one_of_this))
    assert not match(Command('ls brnch', git_not_command))
    assert not match(Command('git branch', git_command))

    assert match(Command('git lock', git_not_command_uncommon))
    assert match(Command('git lock --help', git_not_command_uncommon))

    assert not match(Command('git branch foo', ''))
    assert not match(Command('git checkout feature/test_commit', ''))
    assert not match(Command('git push', ''))


def test_get_new_command(git_not_command, git_not_command_one_of_this,
                         git_not_command_closest, git_not_command_uncommon):
    assert (get_new_command(Command('git brnch', git_not_command))
            == ['git branch'])
    assert (get_new_command(Command('git st', git_not_command_one_of_this))
            == ['git stats', 'git stash', 'git stage'])
    assert (get_new_command(Command('git tags', git_not_command_closest))
            == ['git tag', 'git stage'])

    assert (get_new_command(Command('git lock', git_not_command_uncommon))
            == ['git log'])
    assert (get_new_command(Command('git lock --help', git_not_command_uncommon))
            == ['git log --help'])
