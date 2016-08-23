import pytest
from thefuck.rules.git_add import match, get_new_command
from tests.utils import Command


@pytest.fixture(autouse=True)
def path_exists(mocker):
    return mocker.patch('thefuck.rules.git_add.Path.exists',
                        return_value=True)


@pytest.fixture
def stderr(target):
    return ("error: pathspec '{}' did not match any "
            'file(s) known to git.'.format(target))


@pytest.mark.parametrize('script, target', [
    ('git submodule update unknown', 'unknown'),
    ('git commit unknown', 'unknown')])
def test_match(stderr, script, target):
    assert match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script, target, exists', [
    ('git submodule update known', '', True),
    ('git commit known', '', True),
    ('git submodule update known', stderr, False)])
def test_not_match(path_exists, stderr, script, target, exists):
    path_exists.return_value = exists
    assert not match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script, target, new_command', [
    ('git submodule update unknown', 'unknown',
     'git add -- unknown && git submodule update unknown'),
    ('git commit unknown', 'unknown',
     'git add -- unknown && git commit unknown')])
def test_get_new_command(stderr, script, target, new_command):
    assert get_new_command(Command(script=script, stderr=stderr)) == new_command
