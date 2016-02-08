import pytest
from thefuck.rules.grep_arguments_order import get_new_command, match
from tests.utils import Command

stderr = 'grep: {}: No such file or directory'.format


@pytest.fixture(autouse=True)
def os_path(monkeypatch):
    monkeypatch.setattr('os.path.isfile', lambda x: not x.startswith('-'))


@pytest.mark.parametrize('script, file', [
    ('grep test.py test', 'test'),
    ('grep -lir . test', 'test'),
    ('egrep test.py test', 'test'),
    ('egrep -lir . test', 'test')])
def test_match(script, file):
    assert match(Command(script, stderr=stderr(file)))


@pytest.mark.parametrize('script, stderr', [
    ('cat test.py', stderr('test')),
    ('grep test test.py', ''),
    ('grep -lir test .', ''),
    ('egrep test test.py', ''),
    ('egrep -lir test .', '')])
def test_not_match(script, stderr):
    assert not match(Command(script, stderr=stderr))


@pytest.mark.parametrize('script, stderr, result', [
    ('grep test.py test', stderr('test'), 'grep test test.py'),
    ('grep -lir . test', stderr('test'), 'grep -lir test .'),
    ('grep . test -lir', stderr('test'), 'grep test -lir .'),
    ('egrep test.py test', stderr('test'), 'egrep test test.py'),
    ('egrep -lir . test', stderr('test'), 'egrep -lir test .'),
    ('egrep . test -lir', stderr('test'), 'egrep test -lir .')])
def test_get_new_command(script, stderr, result):
    assert get_new_command(Command(script, stderr=stderr)) == result
