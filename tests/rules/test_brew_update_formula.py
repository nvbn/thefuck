import pytest
from theheck.types import Command
from theheck.rules.brew_update_formula import get_new_command, match


output = ("Error: This command updates brew itself, and does not take formula"
          " names.\nUse `brew upgrade theheck`.")


def test_match():
    command = Command('brew update theheck', output)
    assert match(command)


@pytest.mark.parametrize('script', [
    'brew upgrade foo',
    'brew update'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, formula, ', [
    ('brew update foo', 'foo'),
    ('brew update bar zap', 'bar zap')])
def test_get_new_command(script, formula):
    command = Command(script, output)
    new_command = 'brew upgrade {}'.format(formula)
    assert get_new_command(command) == new_command
