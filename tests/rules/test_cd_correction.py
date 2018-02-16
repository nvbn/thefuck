import pytest
from thefuck.rules.cd_correction import match
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('cd foo', 'cd: foo: No such file or directory'),
    Command('cd foo/bar/baz',
            'cd: foo: No such file or directory'),
    Command('cd foo/bar/baz', 'cd: can\'t cd to foo/bar/baz'),
    Command('cd /foo/bar/', 'cd: The directory "/foo/bar/" does not exist')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('cd foo', ''), Command('', '')])
def test_not_match(command):
    assert not match(command)


# Note that get_new_command uses local filesystem, so not testing it here.
# Instead, see the functional test `functional.test_cd_correction`
