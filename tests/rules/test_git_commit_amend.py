import pytest
from thefuck.rules.git_commit_amend import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('script, code, output', [
    ('git commit -m "test"', '0', 'test output'),
    ('git commit', '0', '')])
def test_match(monkeypatch, output, code, script):
    monkeypatch.setenv('TF_STATUS', code)
    assert match(Command(script, output))


@pytest.mark.parametrize('script, code', [
    ('git branch foo', '0'),
    ('git checkout feature/test_commit', '0'),
    ('git push', '0'),
    ('git commit -m', '1')])
def test_not_match(monkeypatch, script, code):
    monkeypatch.setenv('TF_STATUS', code)
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script', [
    ('git commit -m "test commit"'),
    ('git commit')])
def test_get_new_command(script):
    assert get_new_command(Command(script, '')) == 'git commit --amend'
