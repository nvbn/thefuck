import pytest
from thefuck.rules.ag_literal import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output():
    return ('ERR: Bad regex! pcre_compile() failed at position 1: missing )\n'
            'If you meant to search for a literal string, run ag with -Q\n')


@pytest.mark.parametrize('script', ['ag \\('])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', ['ag foo'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, new_cmd', [
    ('ag \\(', 'ag -Q \\(')])
def test_get_new_command(script, new_cmd, output):
    assert get_new_command((Command(script, output))) == new_cmd
