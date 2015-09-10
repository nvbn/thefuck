import pytest
from thefuck.rules.git_fix_stash import match, get_new_command
from tests.utils import Command


git_stash_err = '''
usage: git stash list [<options>]
   or: git stash show [<stash>]
   or: git stash drop [-q|--quiet] [<stash>]
   or: git stash ( pop | apply ) [--index] [-q|--quiet] [<stash>]
   or: git stash branch <branchname> [<stash>]
   or: git stash [save [--patch] [-k|--[no-]keep-index] [-q|--quiet]
\t\t       [-u|--include-untracked] [-a|--all] [<message>]]
   or: git stash clear
'''


@pytest.mark.parametrize('wrong', [
    'git stash opp',
    'git stash Some message',
    'git stash saev Some message'])
def test_match(wrong):
    assert match(Command(wrong, stderr=git_stash_err))


def test_not_match():
    assert not match(Command("git", stderr=git_stash_err))


@pytest.mark.parametrize('wrong,fixed', [
    ('git stash opp', 'git stash pop'),
    ('git stash Some message', 'git stash save Some message'),
    ('git stash saev Some message', 'git stash save Some message')])
def test_get_new_command(wrong, fixed):
    assert get_new_command(Command(wrong, stderr=git_stash_err)) == fixed
