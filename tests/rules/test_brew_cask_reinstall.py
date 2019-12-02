import pytest
from thefuck.types import Command
from thefuck.rules.brew_cask_reinstall import get_new_command, match


output = ("Warning: Cask 'thefuck' is already installed.\n\nTo "
          "re-install thefuck, run:\n  brew cask reinstall thefuck")


def test_match():
    command = Command('brew cask install thefuck', output)
    assert match(command)


@pytest.mark.parametrize('script', [
    'brew cask reinstall thefuck',
    'brew install foo'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, formula, ', [
    ('brew cask install foo', 'foo'),
    ('brew install bar zap', 'bar zap')])
def test_get_new_command(script, formula):
    command = Command(script, output)
    new_command = 'brew cask reinstall {}'.format(formula)
    assert get_new_command(command) == new_command
