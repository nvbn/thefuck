import pytest
from thefuck.rules.git_rebase_no_changes import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stdout():
    return '''Applying: Test commit
No changes - did you forget to use 'git add'?
If there is nothing left to stage, chances are that something else
already introduced the same changes; you might want to skip this patch.

When you have resolved this problem, run "git rebase --continue".
If you prefer to skip this patch, run "git rebase --skip" instead.
To check out the original branch and stop rebasing, run "git rebase --abort".

'''


def test_match(stdout):
    assert match(Command('git rebase --continue', stdout=stdout))
    assert not match(Command('git rebase --continue'))
    assert not match(Command('git rebase --skip'))


def test_get_new_command(stdout):
    assert (get_new_command(Command('git rebase --continue', stdout=stdout)) ==
            'git rebase --skip')
