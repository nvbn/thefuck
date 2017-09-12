import pytest
from thefuck.types import Command
from thefuck.rules.brew_link import get_new_command, match


@pytest.fixture
def output():
    return ("Error: Could not symlink bin/gcp\n"
            "Target /usr/local/bin/gcp\n"
            "already exists. You may want to remove it:\n"
            "  rm '/usr/local/bin/gcp'\n"
            "\n"
            "To force the link and overwrite all conflicting files:\n"
            "  brew link --overwrite coreutils\n"
            "\n"
            "To list all files that would be deleted:\n"
            "  brew link --overwrite --dry-run coreutils\n")


@pytest.fixture
def new_command(formula):
    return 'brew link --overwrite --dry-run {}'.format(formula)


@pytest.mark.parametrize('script', ['brew link coreutils', 'brew ln coreutils'])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', ['brew link coreutils'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, formula, ', [('brew link coreutils', 'coreutils')])
def test_get_new_command(output, new_command, script, formula):
    assert get_new_command(Command(script, output)) == new_command
