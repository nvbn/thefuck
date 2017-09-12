import pytest
from thefuck.types import Command
from thefuck.rules.brew_uninstall import get_new_command, match


@pytest.fixture
def output():
    return ("Uninstalling /usr/local/Cellar/tbb/4.4-20160916... (118 files, 1.9M)\n"
            "tbb 4.4-20160526, 4.4-20160722 are still installed.\n"
            "Remove all versions with `brew uninstall --force tbb`.\n")


@pytest.fixture
def new_command(formula):
    return 'brew uninstall --force {}'.format(formula)


@pytest.mark.parametrize('script', ['brew uninstall tbb', 'brew rm tbb', 'brew remove tbb'])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', ['brew remove gnuplot'])
def test_not_match(script):
    output = 'Uninstalling /usr/local/Cellar/gnuplot/5.0.4_1... (44 files, 2.3M)\n'
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, formula, ', [('brew uninstall tbb', 'tbb')])
def test_get_new_command(output, new_command, script, formula):
    assert get_new_command(Command(script, output)) == new_command
