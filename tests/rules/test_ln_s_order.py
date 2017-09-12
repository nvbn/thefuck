import pytest
from thefuck.rules.ln_s_order import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def file_exists(mocker):
    return mocker.patch('os.path.exists', return_value=True)


get_output = "ln: failed to create symbolic link '{}': File exists".format


@pytest.mark.parametrize('script, output, exists', [
    ('ln dest source', get_output('source'), True),
    ('ls -s dest source', get_output('source'), True),
    ('ln -s dest source', '', True),
    ('ln -s dest source', get_output('source'), False)])
def test_not_match(file_exists, script, output, exists):
    file_exists.return_value = exists
    assert not match(Command(script, output))


@pytest.mark.usefixtures('file_exists')
@pytest.mark.parametrize('script, result', [
    ('ln -s dest source', 'ln -s source dest'),
    ('ln dest -s source', 'ln -s source dest'),
    ('ln dest source -s', 'ln source -s dest')])
def test_match(script, result):
    output = get_output('source')
    assert match(Command(script, output))
    assert get_new_command(Command(script, output)) == result
