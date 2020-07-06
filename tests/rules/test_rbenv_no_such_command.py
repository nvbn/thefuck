import pytest

from thefuck.rules.rbenv_no_such_command import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output(rbenv_cmd):
    return "rbenv: no such command `{}'".format(rbenv_cmd)


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


@pytest.mark.parametrize('script, rbenv_cmd', [
    ('rbenv globe', 'globe'),
    ('rbenv intall 3.8.0', 'intall'),
    ('rbenv list', 'list'),
])
def test_match(script, rbenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('rbenv global', 'system'),
    ('rbenv versions', '  3.7.0\n  3.7.1\n* 3.7.2\n'),
    ('rbenv install --list', '  3.7.0\n  3.7.1\n  3.7.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))


@pytest.mark.parametrize('script, rbenv_cmd, result', [
    ('rbenv globe', 'globe', 'rbenv global'),
    ('rbenv intall 3.8.0', 'intall', 'rbenv install 3.8.0'),
    ('rbenv list', 'list', 'rbenv install --list'),
    ('rbenv remove 3.8.0', 'remove', 'rbenv uninstall 3.8.0'),
])
def test_get_new_command(script, rbenv_cmd, output, result):
    assert result in get_new_command(Command(script, output))
