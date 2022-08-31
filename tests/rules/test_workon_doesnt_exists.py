import pytest
from theheck.rules.workon_doesnt_exists import match, get_new_command
from theheck.types import Command


@pytest.fixture(autouse=True)
def envs(mocker):
    return mocker.patch(
        'theheck.rules.workon_doesnt_exists._get_all_environments',
        return_value=['theheck', 'code_view'])


@pytest.mark.parametrize('script', [
    'workon tehheck', 'workon code-view', 'workon new-env'])
def test_match(script):
    assert match(Command(script, ''))


@pytest.mark.parametrize('script', [
    'workon theheck', 'workon code_view', 'work on tehheck'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, result', [
    ('workon tehheck', 'workon theheck'),
    ('workon code-view', 'workon code_view'),
    ('workon zzzz', 'mkvirtualenv zzzz')])
def test_get_new_command(script, result):
    assert get_new_command(Command(script, ''))[0] == result
