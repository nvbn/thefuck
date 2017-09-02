import pytest
from thefuck.rules.sudo_command_from_user_path import match, get_new_command
from thefuck.types import Command


output = 'sudo: {}: command not found'


@pytest.fixture(autouse=True)
def which(mocker):
    return mocker.patch('thefuck.rules.sudo_command_from_user_path.which',
                        return_value='/usr/bin/app')


@pytest.mark.parametrize('script, output', [
    ('sudo npm install -g react-native-cli', output.format('npm')),
    ('sudo -u app appcfg update .', output.format('appcfg'))])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output, which_result', [
    ('npm --version', output.format('npm'), '/usr/bin/npm'),
    ('sudo npm --version', '', '/usr/bin/npm'),
    ('sudo npm --version', output.format('npm'), None)])
def test_not_match(which, script, output, which_result):
    which.return_value = which_result
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, output, result', [
    ('sudo npm install -g react-native-cli',
     output.format('npm'),
     'sudo env "PATH=$PATH" npm install -g react-native-cli'),
    ('sudo -u app appcfg update .',
     output.format('appcfg'),
     'sudo -u app env "PATH=$PATH" appcfg update .')])
def test_get_new_command(script, output, result):
    assert get_new_command(Command(script, output)) == result
