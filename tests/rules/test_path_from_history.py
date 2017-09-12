import pytest
from thefuck.rules.path_from_history import match, get_new_command
from thefuck.types import Command


@pytest.fixture(autouse=True)
def history(mocker):
    return mocker.patch(
        'thefuck.rules.path_from_history.get_valid_history_without_current',
        return_value=['cd /opt/java', 'ls ~/work/project/'])


@pytest.fixture(autouse=True)
def path_exists(mocker):
    path_mock = mocker.patch('thefuck.rules.path_from_history.Path')
    exists_mock = path_mock.return_value.expanduser.return_value.exists
    exists_mock.return_value = True
    return exists_mock


@pytest.mark.parametrize('script, output', [
    ('ls project', 'no such file or directory: project'),
    ('cd project', "can't cd to project"),
])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('myapp cats', 'no such file or directory: project'),
    ('cd project', ""),
])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, output, result', [
    ('ls project', 'no such file or directory: project', 'ls ~/work/project'),
    ('cd java', "can't cd to java", 'cd /opt/java'),
])
def test_get_new_command(script, output, result):
    new_command = get_new_command(Command(script, output))
    assert new_command[0] == result
