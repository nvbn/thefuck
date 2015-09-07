import pytest
from thefuck.rules.cp_omitting_directory import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('script, stderr', [
    ('cp dir', 'cp: dor: is a directory'),
    ('cp dir', "cp: omitting directory 'dir'")])
def test_match(script, stderr):
    assert match(Command(script, stderr=stderr))


@pytest.mark.parametrize('script, stderr', [
    ('some dir', 'cp: dor: is a directory'),
    ('some dir', "cp: omitting directory 'dir'"),
    ('cp dir', '')])
def test_not_match(script, stderr):
    assert not match(Command(script, stderr=stderr))


def test_get_new_command():
    assert get_new_command(Command(script='cp dir')) == 'cp -a dir'
