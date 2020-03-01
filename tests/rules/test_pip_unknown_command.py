import pytest
from thefuck.rules.pip_unknown_command import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def pip_unknown_cmd_without_recommend():
    return '''ERROR: unknown command "i"'''


@pytest.fixture
def broken():
    return 'instatl'


@pytest.fixture
def suggested():
    return 'install'


@pytest.fixture
def pip_unknown_cmd(broken, suggested):
    return 'ERROR: unknown command "{}" - maybe you meant "{}"'.format(broken, suggested)


def test_match(pip_unknown_cmd, pip_unknown_cmd_without_recommend):
    assert match(Command('pip instatl', pip_unknown_cmd))
    assert not match(Command('pip i',
                             pip_unknown_cmd_without_recommend))


@pytest.mark.parametrize('script, broken, suggested, new_cmd', [
    ('pip un+install thefuck', 'un+install', 'uninstall', 'pip uninstall thefuck'),
    ('pip instatl', 'instatl', 'install', 'pip install')])
def test_get_new_command(script, new_cmd, pip_unknown_cmd):
    assert get_new_command(Command(script,
                                   pip_unknown_cmd)) == new_cmd
