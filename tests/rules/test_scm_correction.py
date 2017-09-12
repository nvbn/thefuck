import pytest
from thefuck.rules.scm_correction import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def get_actual_scm_mock(mocker):
    return mocker.patch('thefuck.rules.scm_correction._get_actual_scm',
                        return_value=None)


@pytest.mark.parametrize('script, output, actual_scm', [
    ('git log', 'fatal: Not a git repository '
                '(or any of the parent directories): .git',
     'hg'),
    ('hg log', "abort: no repository found in '/home/nvbn/exp/thefuck' "
               "(.hg not found)!",
     'git')])
def test_match(get_actual_scm_mock, script, output, actual_scm):
    get_actual_scm_mock.return_value = actual_scm
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output, actual_scm', [
    ('git log', '', 'hg'),
    ('git log', 'fatal: Not a git repository '
                '(or any of the parent directories): .git',
     None),
    ('hg log', "abort: no repository found in '/home/nvbn/exp/thefuck' "
               "(.hg not found)!",
     None),
    ('not-scm log', "abort: no repository found in '/home/nvbn/exp/thefuck' "
                    "(.hg not found)!",
     'git')])
def test_not_match(get_actual_scm_mock, script, output, actual_scm):
    get_actual_scm_mock.return_value = actual_scm
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, actual_scm, result', [
    ('git log', 'hg', 'hg log'),
    ('hg log', 'git', 'git log')])
def test_get_new_command(get_actual_scm_mock, script, actual_scm, result):
    get_actual_scm_mock.return_value = actual_scm
    new_command = get_new_command(Command(script, ''))
    assert new_command == result
