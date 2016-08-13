import pytest
from thefuck.rules.gradle_wrapper import match, get_new_command
from tests.utils import Command


@pytest.fixture(autouse=True)
def exists(mocker):
    return mocker.patch('thefuck.rules.gradle_wrapper.os.path.isfile',
                        return_value=True)


@pytest.mark.parametrize('command', [
    Command('gradle tasks', stderr='gradle: not found'),
    Command('gradle build', stderr='gradle: not found')])
def test_match(mocker, command):
    mocker.patch('thefuck.rules.gradle_wrapper.which', return_value=None)

    assert match(command)


@pytest.mark.parametrize('command, gradlew, which', [
    (Command('gradle tasks', stderr='gradle: not found'), False, None),
    (Command('gradle tasks', stderr='command not found'), True, '/usr/bin/gradle'),
    (Command('npm tasks', stderr='npm: not found'), True, None)])
def test_not_match(mocker, exists, command, gradlew, which):
    mocker.patch('thefuck.rules.gradle_wrapper.which', return_value=which)
    exists.return_value = gradlew

    assert not match(command)


@pytest.mark.parametrize('script, result', [
    ('gradle assemble', './gradlew assemble'),
    ('gradle --help', './gradlew --help'),
    ('gradle build -c', './gradlew build -c')])
def test_get_new_command(script, result):
    command = Command(script)
    assert get_new_command(command) == result
