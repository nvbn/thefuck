import pytest
from io import BytesIO
from thefuck.types import Command
from thefuck.rules.gulp_not_task import match, get_new_command


def output(task):
    return '''[00:41:11] Using gulpfile gulpfile.js
[00:41:11] Task '{}' is not in your gulpfile
[00:41:11] Please check the documentation for proper gulpfile formatting
'''.format(task)


def test_match():
    assert match(Command('gulp srve', output('srve')))


@pytest.mark.parametrize('script, stdout', [
    ('gulp serve', ''),
    ('cat srve', output('srve'))])
def test_not_march(script, stdout):
    assert not match(Command(script, stdout))


def test_get_new_command(mocker):
    mock = mocker.patch('subprocess.Popen')
    mock.return_value.stdout = BytesIO(b'serve \nbuild \ndefault \n')
    command = Command('gulp srve', output('srve'))
    assert get_new_command(command) == ['gulp serve', 'gulp default']
