import pytest
from thefuck.specific.git import git_support
from thefuck.types import Command


@pytest.mark.parametrize('called, command, output', [
    ('git co', 'git checkout', "19:22:36.299340 git.c:282   trace: alias expansion: co => 'checkout'"),
    ('git com file', 'git commit --verbose file',
     "19:23:25.470911 git.c:282   trace: alias expansion: com => 'commit' '--verbose'"),
    ('git com -m "Initial commit"', 'git commit -m "Initial commit"',
     "19:22:36.299340 git.c:282   trace: alias expansion: com => 'commit'"),
    ('git br -d some_branch', 'git branch -d some_branch',
     "19:22:36.299340 git.c:282   trace: alias expansion: br => 'branch'")])
def test_git_support(called, command, output):
    @git_support
    def fn(command):
        return command.script

    assert fn(Command(called, output)) == command


@pytest.mark.parametrize('command, is_git', [
    ('git pull', True),
    ('hub pull', True),
    ('git push --set-upstream origin foo', True),
    ('hub push --set-upstream origin foo', True),
    ('ls', False),
    ('cat git', False),
    ('cat hub', False)])
@pytest.mark.parametrize('output', ['', None])
def test_git_support_match(command, is_git, output):
    @git_support
    def fn(command):
        return True

    assert fn(Command(command, output)) == is_git
