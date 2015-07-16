import pytest
from mock import Mock
from thefuck.utils import git_support, sudo_support, wrap_settings, memoize, get_closest
from thefuck.types import Settings
from tests.utils import Command


@pytest.mark.parametrize('override, old, new', [
    ({'key': 'val'}, {}, {'key': 'val'}),
    ({'key': 'new-val'}, {'key': 'val'}, {'key': 'new-val'})])
def test_wrap_settings(override, old, new):
    fn = lambda _, settings: settings
    assert wrap_settings(override)(fn)(None, Settings(old)) == new


@pytest.mark.parametrize('return_value, command, called, result', [
    ('ls -lah', 'sudo ls', 'ls', 'sudo ls -lah'),
    ('ls -lah', 'ls', 'ls', 'ls -lah'),
    (True, 'sudo ls', 'ls', True),
    (True, 'ls', 'ls', True),
    (False, 'sudo ls', 'ls', False),
    (False, 'ls', 'ls', False)])
def test_sudo_support(return_value, command, called, result):
    fn = Mock(return_value=return_value, __name__='')
    assert sudo_support(fn)(Command(command), None) == result
    fn.assert_called_once_with(Command(called), None)


@pytest.mark.parametrize('called, command, stderr', [
    ('git co', "git 'checkout'", "19:22:36.299340 git.c:282   trace: alias expansion: co => 'checkout'"),
    ('git com file', "git 'commit' '--verbose' file", "19:23:25.470911 git.c:282   trace: alias expansion: com => 'commit' '--verbose'")])
def test_git_support(called, command, stderr):
    @git_support
    def fn(command, settings): return command.script
    assert fn(Command(script=called, stderr=stderr), None) == command


def test_memoize():
    fn = Mock(__name__='fn')
    memoized = memoize(fn)
    memoized()
    memoized()
    fn.assert_called_once_with()


@pytest.mark.usefixtures('no_memoize')
def test_no_memoize():
    fn = Mock(__name__='fn')
    memoized = memoize(fn)
    memoized()
    memoized()
    assert fn.call_count == 2


class TestGetClosest(object):

    def test_when_can_match(self):
        assert 'branch' == get_closest('brnch', ['branch', 'status'])

    def test_when_cant_match(self):
        assert 'status' == get_closest('st', ['status', 'reset'])
