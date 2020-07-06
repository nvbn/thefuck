import pytest

from thefuck.rules.goenv_no_such_command import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output(goenv_cmd):
    return "goenv: no such command '{}'".format(goenv_cmd)


@pytest.fixture(autouse=True)
def Popen(mocker):
    mock = mocker.patch('thefuck.rules.goenv_no_such_command.Popen')
    mock.return_value.stdout.readlines.return_value = (
        b'--version\nactivate\ncommands\ncompletions\ndeactivate\nexec_\n'
        b'global\nhelp\nhooks\ninit\ninstall\nlocal\nprefix_\n'
        b'realpath.dylib\nrehash\nroot\nshell\nshims\nuninstall\nversion_\n'
        b'version-file\nversion-file-read\nversion-file-write\nversion-name_\n'
        b'version-origin\nversions\nvirtualenv\nvirtualenv-delete_\n'
        b'virtualenv-init\nvirtualenv-prefix\nvirtualenvs_\n'
        b'virtualenvwrapper\nvirtualenvwrapper_lazy\nwhence\nwhich_\n'
    ).split()
    return mock


@pytest.mark.parametrize('script, goenv_cmd', [
    ('goenv globe', 'globe'),
    ('goenv intall 3.8.0', 'intall'),
    ('goenv list', 'list'),
])
def test_match(script, goenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('goenv global', 'system'),
    ('goenv versions', '  3.7.0\n  3.7.1\n* 3.7.2\n'),
    ('goenv install --list', '  3.7.0\n  3.7.1\n  3.7.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))


@pytest.mark.parametrize('script, goenv_cmd, result', [
    ('goenv globe', 'globe', 'goenv global'),
    ('goenv intall 3.8.0', 'intall', 'goenv install 3.8.0'),
    ('goenv list', 'list', 'goenv install --list'),
    ('goenv remove 3.8.0', 'remove', 'goenv uninstall 3.8.0'),
])
def test_get_new_command(script, goenv_cmd, output, result):
    assert result in get_new_command(Command(script, output))
