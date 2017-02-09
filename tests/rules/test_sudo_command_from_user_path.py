import pytest
from thefuck.rules.sudo_command_from_user_path import match, get_new_command
from tests.utils import Command


stderr = 'sudo: {}: command not found'


@pytest.fixture(autouse=True)
def which(mocker):
    return mocker.patch('thefuck.rules.sudo_command_from_user_path.which',
                        return_value='/usr/bin/app')


@pytest.mark.parametrize('script, stderr', [
    ('sudo npm install -g react-native-cli', stderr.format('npm')),
    ('sudo -u app appcfg update .', stderr.format('appcfg'))])
def test_match(script, stderr):
    assert match(Command(script, stderr=stderr))


@pytest.mark.parametrize('script, stderr, which_result', [
    ('npm --version', stderr.format('npm'), '/usr/bin/npm'),
    ('sudo npm --version', '', '/usr/bin/npm'),
    ('sudo npm --version', stderr.format('npm'), None)])
def test_not_match(which, script, stderr, which_result):
    which.return_value = which_result
    assert not match(Command(script, stderr=stderr))


@pytest.mark.parametrize('script, stderr, result', [
    ('sudo npm install -g react-native-cli',
     stderr.format('npm'),
     'sudo env "PATH=$PATH" npm install -g react-native-cli'),
    ('sudo -u app appcfg update .',
     stderr.format('appcfg'),
     'sudo -u app env "PATH=$PATH" appcfg update .')])
def test_get_new_command(script, stderr, result):
    assert get_new_command(Command(script, stderr=stderr)) == result
