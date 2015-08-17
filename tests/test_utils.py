import pytest
from mock import Mock
from thefuck.utils import git_support, sudo_support, wrap_settings,\
    memoize, get_closest, get_all_executables, replace_argument, \
    get_all_matched_commands
from thefuck.types import Settings
from tests.utils import Command


@pytest.mark.parametrize('override, old, new', [
    ({'key': 'val'}, {}, {'key': 'val'}),
    ({'key': 'new-val'}, {'key': 'val'}, {'key': 'val'}),
    ({'key': 'new-val', 'unset': 'unset'}, {'key': 'val'}, {'key': 'val', 'unset': 'unset'})])
def test_wrap_settings(override, old, new):
    fn = lambda _, settings: settings
    assert wrap_settings(override)(fn)(None, Settings(old)) == new


@pytest.mark.parametrize('return_value, command, called, result', [
    ('ls -lah', 'sudo ls', 'ls', 'sudo ls -lah'),
    ('ls -lah', 'ls', 'ls', 'ls -lah'),
    (['ls -lah'], 'sudo ls', 'ls', ['sudo ls -lah']),
    (True, 'sudo ls', 'ls', True),
    (True, 'ls', 'ls', True),
    (False, 'sudo ls', 'ls', False),
    (False, 'ls', 'ls', False)])
def test_sudo_support(return_value, command, called, result):
    fn = Mock(return_value=return_value, __name__='')
    assert sudo_support(fn)(Command(command), None) == result
    fn.assert_called_once_with(Command(called), None)


@pytest.mark.parametrize('called, command, stderr', [
    ('git co', 'git checkout', "19:22:36.299340 git.c:282   trace: alias expansion: co => 'checkout'"),
    ('git com file', 'git commit --verbose file', "19:23:25.470911 git.c:282   trace: alias expansion: com => 'commit' '--verbose'")])
def test_git_support(called, command, stderr):
    @git_support
    def fn(command, settings): return command.script
    assert fn(Command(script=called, stderr=stderr), None) == command


@pytest.mark.parametrize('command, is_git', [
    ('git pull', True),
    ('hub pull', True),
    ('git push --set-upstream origin foo', True),
    ('hub push --set-upstream origin foo', True),
    ('ls', False),
    ('cat git', False),
    ('cat hub', False)])
def test_git_support_match(command, is_git):
    @git_support
    def fn(command, settings): return True
    assert fn(Command(script=command), None) == is_git


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

    def test_without_fallback(self):
        assert get_closest('st', ['status', 'reset'],
                           fallback_to_first=False) is None


@pytest.fixture
def get_aliases(mocker):
    mocker.patch('thefuck.shells.get_aliases',
                 return_value=['vim', 'apt-get', 'fsck', 'fuck'])


@pytest.mark.usefixtures('no_memoize', 'get_aliases')
def test_get_all_callables():
    all_callables = get_all_executables()
    assert 'vim' in all_callables
    assert 'fsck' in all_callables
    assert 'fuck' not in all_callables


@pytest.mark.parametrize('args, result', [
    (('apt-get instol vim', 'instol', 'install'), 'apt-get install vim'),
    (('git brnch', 'brnch', 'branch'), 'git branch')])
def test_replace_argument(args, result):
    assert replace_argument(*args) == result


@pytest.mark.parametrize('stderr, result', [
    (("git: 'cone' is not a git command. See 'git --help'.\n"
      '\n'
      'Did you mean one of these?\n'
      '\tclone'), ['clone']),
    (("git: 're' is not a git command. See 'git --help'.\n"
      '\n'
      'Did you mean one of these?\n'
      '\trebase\n'
      '\treset\n'
      '\tgrep\n'
      '\trm'), ['rebase', 'reset', 'grep', 'rm']),
    (('tsuru: "target" is not a tsuru command. See "tsuru help".\n'
      '\n'
      'Did you mean one of these?\n'
      '\tservice-add\n'
      '\tservice-bind\n'
      '\tservice-doc\n'
      '\tservice-info\n'
      '\tservice-list\n'
      '\tservice-remove\n'
      '\tservice-status\n'
      '\tservice-unbind'), ['service-add', 'service-bind', 'service-doc',
                            'service-info', 'service-list', 'service-remove',
                            'service-status', 'service-unbind'])])
def test_get_all_matched_commands(stderr, result):
    assert list(get_all_matched_commands(stderr)) == result
