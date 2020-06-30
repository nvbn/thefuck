import pytest

from thefuck.rules.nodenv_no_such_command import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output(nodenv_cmd):
    return "nodenv: no such command `{}'".format(nodenv_cmd)


@pytest.fixture(autouse=True)
def Popen(mocker):
    mock = mocker.patch('thefuck.rules.nodenv_no_such_command.Popen')
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


@pytest.mark.parametrize('script, nodenv_cmd', [
    ('nodenv globe', 'globe'),
    ('nodenv intall 3.8.0', 'intall'),
    ('nodenv list', 'list'),
])
def test_match(script, nodenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('nodenv global', 'system'),
    ('nodenv versions', '  3.7.0\n  3.7.1\n* 3.7.2\n'),
    ('nodenv install --list', '  3.7.0\n  3.7.1\n  3.7.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))


@pytest.mark.parametrize('script, nodenv_cmd, result', [
    ('nodenv globe', 'globe', 'nodenv global'),
    ('nodenv intall 3.8.0', 'intall', 'nodenv install 3.8.0'),
    ('nodenv list', 'list', 'nodenv install --list'),
    ('nodenv remove 3.8.0', 'remove', 'nodenv uninstall 3.8.0'),
])
def test_get_new_command(script, nodenv_cmd, output, result):
    assert result in get_new_command(Command(script, output))
