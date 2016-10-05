import pytest
from thefuck.rules.ag_literal import get_new_command, match
from tests.utils import Command


@pytest.fixture
def stderr():
    return ('ERR: Bad regex! pcre_compile() failed at position 1: missing )\n'
            'If you meant to search for a literal string, run ag with -Q\n')


@pytest.mark.parametrize('script', ['ag \('])
def test_match(script, stderr):
    assert match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script', ['ag foo'])
def test_not_match(script):
    assert not match(Command(script=script))


@pytest.mark.parametrize('script, new_cmd', [
    ('ag \(', 'ag -Q \(')])
def test_get_new_command(script, new_cmd, stderr):
    assert get_new_command((Command(script=script, stderr=stderr))) == new_cmd
