import pytest
from tests.utils import Command
from thefuck.rules.brew_update_formula import get_new_command, match


@pytest.fixture
def stderr():
    return ("Error: This command updates brew itself, and does not take formula"
            " names.\nUse 'brew upgrade <formula>'.")


@pytest.fixture
def new_command(formula):
    return 'brew upgrade {}'.format(formula)


@pytest.mark.parametrize('script', ['brew update foo', 'brew update bar zap'])
def test_match(stderr, script):
    assert match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script', ['brew upgrade foo', 'brew update'])
def test_not_match(script):
    assert not match(Command(script=script, stderr=''))


@pytest.mark.parametrize('script, formula, ', [
    ('brew update foo', 'foo'), ('brew update bar zap', 'bar zap')])
def test_get_new_command(stderr, new_command, script, formula):
    assert get_new_command(Command(script=script, stderr=stderr)) == new_command
