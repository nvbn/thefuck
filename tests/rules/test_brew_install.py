import pytest
from thefuck.rules.brew_install import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def brew_no_available_formula():
    return '''Warning: No available formula with the name "gitt". Did you mean git, gitg or gist?'''


@pytest.fixture
def brew_install_no_argument():
    return '''Install a formula or cask. Additional options specific to a formula may be'''


@pytest.fixture
def brew_already_installed():
    return '''Warning: git-2.3.5 already installed'''


def test_match(brew_no_available_formula, brew_already_installed,
               brew_install_no_argument):
    assert match(Command('brew install gitt',
                         brew_no_available_formula))
    assert not match(Command('brew install git',
                             brew_already_installed))
    assert not match(Command('brew install', brew_install_no_argument))


def test_get_new_command(brew_no_available_formula):
    assert get_new_command(Command('brew install gitt',
                                   brew_no_available_formula))\
        == 'brew install git'

    assert get_new_command(Command('brew install aa',
                                   brew_no_available_formula))\
        != 'brew install aha'
