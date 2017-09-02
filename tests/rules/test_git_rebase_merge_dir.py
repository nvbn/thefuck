import pytest
from thefuck.rules.git_rebase_merge_dir import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return ('\n\nIt seems that there is already a rebase-merge directory, and\n'
            'I wonder if you are in the middle of another rebase.  If that is the\n'
            'case, please try\n'
            '\tgit rebase (--continue | --abort | --skip)\n'
            'If that is not the case, please\n'
            '\trm -fr "/foo/bar/baz/egg/.git/rebase-merge"\n'
            'and run me again.  I am stopping in case you still have something\n'
            'valuable there.\n')


@pytest.mark.parametrize('script', [
    'git rebase master',
    'git rebase -skip',
    'git rebase'])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', ['git rebase master', 'git rebase -abort'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, result', [
    ('git rebase master', [
        'git rebase --abort', 'git rebase --skip', 'git rebase --continue',
        'rm -fr "/foo/bar/baz/egg/.git/rebase-merge"']),
    ('git rebase -skip', [
        'git rebase --skip', 'git rebase --abort', 'git rebase --continue',
        'rm -fr "/foo/bar/baz/egg/.git/rebase-merge"']),
    ('git rebase', [
        'git rebase --skip', 'git rebase --abort', 'git rebase --continue',
        'rm -fr "/foo/bar/baz/egg/.git/rebase-merge"'])])
def test_get_new_command(output, script, result):
    assert get_new_command(Command(script, output)) == result
