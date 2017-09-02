import pytest
from thefuck.types import Command
from thefuck.rules.brew_update_formula import get_new_command, match


@pytest.fixture
def output():
    return ("Error: This command updates brew itself, and does not take formula"
            " names.\nUse 'brew upgrade <formula>'.")


@pytest.fixture
def new_command(formula):
    return 'brew upgrade {}'.format(formula)


@pytest.mark.parametrize('script', ['brew update foo', 'brew update bar zap'])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', ['brew upgrade foo', 'brew update'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, formula, ', [
    ('brew update foo', 'foo'), ('brew update bar zap', 'bar zap')])
def test_get_new_command(output, new_command, script, formula):
    assert get_new_command(Command(script, output)) == new_command
