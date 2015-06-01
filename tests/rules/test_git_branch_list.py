from thefuck import shells
from thefuck.rules.git_branch_list import match, get_new_command
from tests.utils import Command

def test_match():
    assert match(Command('git branch list'), None)


def test_not_match():
    assert not match(Command(), None)
    assert not match(Command('git commit'), None)
    assert not match(Command('git branch'), None)
    assert not match(Command('git stash list'), None)


def test_get_new_command():
    assert (get_new_command(Command('git branch list'), None) ==
            shells.and_('git branch --delete list', 'git branch'))
