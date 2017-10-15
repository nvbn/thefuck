import pytest
from thefuck.rules.prove_recursively import match, get_new_command
from thefuck.types import Command


output = '''Files=0, Tests=0,  0 wallclock secs ( 0.00 usr +  0.00 sys =  0.00 CPU)
Result: NOTESTS'''


@pytest.fixture
def isdir(mocker):
    return mocker.patch('thefuck.rules.prove_recursively'
                        '.os.path.isdir')


@pytest.mark.parametrize('script, output', [
    ('prove -lv t', output),
    ('prove app/t', output)])
def test_match(isdir, script, output):
    isdir.return_value = True
    command = Command(script, output)
    assert match(command)


@pytest.mark.parametrize('script, output, isdir_result', [
    ('prove -lv t', output, False),
    ('prove -r t', output, True),
    ('prove --recurse t', output, True)])
def test_not_match(isdir, script, output, isdir_result):
    isdir.return_value = isdir_result
    command = Command(script, output)
    assert not match(command)


@pytest.mark.parametrize('before, after', [
    ('prove -lv t', 'prove -r -lv t'),
    ('prove t', 'prove -r t')])
def test_get_new_command(before, after):
    command = Command(before, output)
    assert get_new_command(command) == after
