import pytest
from thefuck.rules.ln_s_order import match, get_new_command
from tests.utils import Command


@pytest.fixture
def file_exists(mocker):
    return mocker.patch('os.path.exists', return_value=True)


get_stderr = "ln: failed to create symbolic link '{}': File exists".format


@pytest.mark.usefixtures('file_exists')
@pytest.mark.parametrize('script', [
    'ln -s dest source',
    'ln dest -s source',
    'ln dest source -s'])
def test_match(script):
    stderr = get_stderr('source')
    assert match(Command(script, stderr=stderr))


@pytest.mark.parametrize('script, stderr, exists', [
    ('ln dest source', get_stderr('source'), True),
    ('ls -s dest source', get_stderr('source'), True),
    ('ln -s dest source', '', True),
    ('ln -s dest source', get_stderr('source'), False)])
def test_not_match(file_exists, script, stderr, exists):
    file_exists.return_value = exists
    assert not match(Command(script, stderr=stderr))


@pytest.mark.usefixtures('file_exists')
@pytest.mark.parametrize('script, result', [
    ('ln -s dest source', 'ln -s source dest'),
    ('ln dest -s source', 'ln -s source dest'),
    ('ln dest source -s', 'ln source -s dest')])
def test_match(script, result):
    stderr = get_stderr('source')
    assert get_new_command(Command(script, stderr=stderr)) == result
