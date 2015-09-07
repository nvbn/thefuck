from thefuck import shells
from thefuck.rules.git_branch_list import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('git branch list'))


def test_not_match():
    assert not match(Command())
    assert not match(Command('git commit'))
    assert not match(Command('git branch'))
    assert not match(Command('git stash list'))


def test_get_new_command():
    assert (get_new_command(Command('git branch list')) ==
            shells.and_('git branch --delete list', 'git branch'))
