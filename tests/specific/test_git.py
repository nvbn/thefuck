import pytest
from thefuck.specific.git import git_support
from tests.utils import Command


@pytest.mark.parametrize('called, command, stderr', [
    ('git co', 'git checkout', "19:22:36.299340 git.c:282   trace: alias expansion: co => 'checkout'"),
    ('git com file', 'git commit --verbose file',
     "19:23:25.470911 git.c:282   trace: alias expansion: com => 'commit' '--verbose'")])
def test_git_support(called, command, stderr):
    @git_support
    def fn(command):
        return command.script

    assert fn(Command(script=called, stderr=stderr)) == command


@pytest.mark.parametrize('command, is_git', [
    ('git pull', True),
    ('hub pull', True),
    ('git push --set-upstream origin foo', True),
    ('hub push --set-upstream origin foo', True),
    ('ls', False),
    ('cat git', False),
    ('cat hub', False)])
def test_git_support_match(command, is_git):
    @git_support
    def fn(command):
        return True

    assert fn(Command(script=command)) == is_git
