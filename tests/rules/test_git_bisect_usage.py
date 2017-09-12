import pytest
from thefuck.types import Command
from thefuck.rules.git_bisect_usage import match, get_new_command


@pytest.fixture
def output():
    return ("usage: git bisect [help|start|bad|good|new|old"
            "|terms|skip|next|reset|visualize|replay|log|run]")


@pytest.mark.parametrize('script', [
    'git bisect strt', 'git bisect rset', 'git bisect goood'])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', [
    'git bisect', 'git bisect start', 'git bisect good'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, new_cmd, ', [
    ('git bisect goood', ['good', 'old', 'log']),
    ('git bisect strt', ['start', 'terms', 'reset']),
    ('git bisect rset', ['reset', 'next', 'start'])])
def test_get_new_command(output, script, new_cmd):
    new_cmd = ['git bisect %s' % cmd for cmd in new_cmd]
    assert get_new_command(Command(script, output)) == new_cmd
