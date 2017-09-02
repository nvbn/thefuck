import pytest
from thefuck.rules.git_add import match, get_new_command
from thefuck.types import Command


@pytest.fixture(autouse=True)
def path_exists(mocker):
    return mocker.patch('thefuck.rules.git_add.Path.exists',
                        return_value=True)


@pytest.fixture
def output(target):
    return ("error: pathspec '{}' did not match any "
            'file(s) known to git.'.format(target))


@pytest.mark.parametrize('script, target', [
    ('git submodule update unknown', 'unknown'),
    ('git commit unknown', 'unknown')])
def test_match(output, script, target):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, target, exists', [
    ('git submodule update known', '', True),
    ('git commit known', '', True),
    ('git submodule update known', output, False)])
def test_not_match(path_exists, output, script, target, exists):
    path_exists.return_value = exists
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, target, new_command', [
    ('git submodule update unknown', 'unknown',
     'git add -- unknown && git submodule update unknown'),
    ('git commit unknown', 'unknown',
     'git add -- unknown && git commit unknown')])
def test_get_new_command(output, script, target, new_command):
    assert get_new_command(Command(script, output)) == new_command
