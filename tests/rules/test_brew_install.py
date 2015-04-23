import pytest
from thefuck.types import Command
from thefuck.rules.brew_install import match, get_new_command
from thefuck.rules.brew_install import brew_formulas


@pytest.fixture
def brew_no_available_formula():
    return '''Error: No available formula for elsticsearch '''


@pytest.fixture
def brew_install_no_argument():
    return '''This command requires a formula argument'''


@pytest.fixture
def brew_already_installed():
    return '''Warning: git-2.3.5 already installed'''


def _is_not_okay_to_test():
    if 'elasticsearch' not in brew_formulas:
        return True
    return False


@pytest.mark.skipif(_is_not_okay_to_test(),
                    reason='No need to run if there\'s no formula')
def test_match(brew_no_available_formula, brew_already_installed,
               brew_install_no_argument):
    assert match(Command('brew install elsticsearch', '',
                         brew_no_available_formula), None)
    assert not match(Command('brew install git', '',
                             brew_already_installed), None)
    assert not match(Command('brew install', '', brew_install_no_argument),
                     None)


@pytest.mark.skipif(_is_not_okay_to_test(),
                    reason='No need to run if there\'s no formula')
def test_get_new_command(brew_no_available_formula):
    assert get_new_command(Command('brew install elsticsearch', '',
                                   brew_no_available_formula), None)\
        == 'brew install elasticsearch'

    assert get_new_command(Command('brew install aa', '',
                                   brew_no_available_formula),
                           None) != 'brew install aha'
