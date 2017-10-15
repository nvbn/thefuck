import pytest
from thefuck.rules.git_push_different_branch_names import get_new_command, match
from thefuck.types import Command


output = """fatal: The upstream branch of your current branch does not match
the name of your current branch.  To push to the upstream branch
on the remote, use

    git push origin HEAD:%s

To push to the branch of the same name on the remote, use

    git push origin %s

To choose either option permanently, see push.default in 'git help config'.
"""


def error_msg(localbranch, remotebranch):
    return output % (remotebranch, localbranch)


def test_match():
    assert match(Command('git push', error_msg('foo', 'bar')))


@pytest.mark.parametrize('command', [
    Command('vim', ''),
    Command('git status', error_msg('foo', 'bar')),
    Command('git push', '')
])
def test_not_match(command):
    assert not match(command)


def test_get_new_command():
    new_command = get_new_command(Command('git push', error_msg('foo', 'bar')))
    assert new_command == 'git push origin HEAD:bar'
