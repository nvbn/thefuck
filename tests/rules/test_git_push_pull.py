import pytest
from thefuck.rules.git_push_pull import match, get_new_command
from thefuck.types import Command


git_err = '''
To /tmp/foo
 ! [rejected]        master -> master (non-fast-forward)
 error: failed to push some refs to '/tmp/bar'
 hint: Updates were rejected because the tip of your current branch is behind
 hint: its remote counterpart. Integrate the remote changes (e.g.
 hint: 'git pull ...') before pushing again.
 hint: See the 'Note about fast-forwards' in 'git push --help' for details.
'''

git_err2 = '''
To /tmp/foo
 ! [rejected]        master -> master (non-fast-forward)
 error: failed to push some refs to '/tmp/bar'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first integrate the remote changes
hint: (e.g., 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
'''

git_uptodate = 'Everything up-to-date'
git_ok = '''
Counting objects: 3, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 282 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To /tmp/bar
   514eed3..f269c79  master -> master
'''


@pytest.mark.parametrize('command', [
    Command('git push', git_err),
    Command('git push nvbn', git_err),
    Command('git push nvbn master', git_err),
    Command('git push', git_err2),
    Command('git push nvbn', git_err2),
    Command('git push nvbn master', git_err2)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('git push', git_ok),
    Command('git push', git_uptodate),
    Command('git push nvbn', git_ok),
    Command('git push nvbn master', git_uptodate),
    Command('git push nvbn', git_ok),
    Command('git push nvbn master', git_uptodate)])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, output', [
    (Command('git push', git_err), 'git pull && git push'),
    (Command('git push nvbn', git_err),
     'git pull nvbn && git push nvbn'),
    (Command('git push nvbn master', git_err),
     'git pull nvbn master && git push nvbn master'),
    (Command('git push', git_err2), 'git pull && git push'),
    (Command('git push nvbn', git_err2),
     'git pull nvbn && git push nvbn'),
    (Command('git push nvbn master', git_err2),
     'git pull nvbn master && git push nvbn master')])
def test_get_new_command(command, output):
    assert get_new_command(command) == output
