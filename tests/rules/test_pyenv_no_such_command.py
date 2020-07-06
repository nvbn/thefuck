import pytest

from thefuck.rules.pyenv_no_such_command import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output(pyenv_cmd):
    return "pyenv: no such command `{}'".format(pyenv_cmd)


@pytest.fixture(autouse=True)
def Popen(mocker):
    mock = mocker.patch('thefuck.rules.pyenv_no_such_command.Popen')
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


@pytest.mark.parametrize('script, pyenv_cmd', [
    ('pyenv globe', 'globe'),
    ('pyenv intall 3.8.0', 'intall'),
    ('pyenv list', 'list'),
])
def test_match(script, pyenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('pyenv global', 'system'),
    ('pyenv versions', '  3.7.0\n  3.7.1\n* 3.7.2\n'),
    ('pyenv install --list', '  3.7.0\n  3.7.1\n  3.7.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))


@pytest.mark.parametrize('script, pyenv_cmd, result', [
    ('pyenv globe', 'globe', 'pyenv global'),
    ('pyenv intall 3.8.0', 'intall', 'pyenv install 3.8.0'),
    ('pyenv list', 'list', 'pyenv install --list'),
    ('pyenv remove 3.8.0', 'remove', 'pyenv uninstall 3.8.0'),
])
def test_get_new_command(script, pyenv_cmd, output, result):
    assert result in get_new_command(Command(script, output))
