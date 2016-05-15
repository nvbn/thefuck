# -*- coding: utf-8 -*-

import pytest
import warnings
from mock import Mock
import six
from thefuck.utils import default_settings, \
    memoize, get_closest, get_all_executables, replace_argument, \
    get_all_matched_commands, is_app, for_app, cache, compatibility_call, \
    get_valid_history_without_current
from tests.utils import Command


@pytest.mark.parametrize('override, old, new', [
    ({'key': 'val'}, {}, {'key': 'val'}),
    ({'key': 'new-val'}, {'key': 'val'}, {'key': 'val'}),
    ({'key': 'new-val', 'unset': 'unset'}, {'key': 'val'}, {'key': 'val', 'unset': 'unset'})])
def test_default_settings(settings, override, old, new):
    settings.clear()
    settings.update(old)
    fn = lambda _: _
    default_settings(override)(fn)(None)
    assert settings == new


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
    mocker.patch('thefuck.shells.shell.get_aliases',
                 return_value=['vim', 'apt-get', 'fsck', 'fuck'])


@pytest.mark.usefixtures('no_memoize', 'get_aliases')
def test_get_all_executables():
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


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('script, names, result', [
    ('git diff', ['git', 'hub'], True),
    ('hub diff', ['git', 'hub'], True),
    ('hg diff', ['git', 'hub'], False)])
def test_is_app(script, names, result):
    assert is_app(Command(script), *names) == result


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('script, names, result', [
    ('git diff', ['git', 'hub'], True),
    ('hub diff', ['git', 'hub'], True),
    ('hg diff', ['git', 'hub'], False)])
def test_for_app(script, names, result):
    @for_app(*names)
    def match(command):
        return True

    assert match(Command(script)) == result


class TestCache(object):
    @pytest.fixture(autouse=True)
    def enable_cache(self, monkeypatch):
        monkeypatch.setattr('thefuck.utils.cache.disabled', False)

    @pytest.fixture
    def shelve(self, mocker):
        value = {}

        class _Shelve(object):
            def __init__(self, path):
                pass

            def __setitem__(self, k, v):
                value[k] = v

            def __getitem__(self, k):
                return value[k]

            def get(self, k, v=None):
                return value.get(k, v)

            def close(self):
                return

        mocker.patch('thefuck.utils.shelve.open', new_callable=lambda: _Shelve)
        return value

    @pytest.fixture(autouse=True)
    def mtime(self, mocker):
        mocker.patch('thefuck.utils.os.path.getmtime', return_value=0)

    @pytest.fixture
    def fn(self):
        @cache('~/.bashrc')
        def fn():
            return 'test'

        return fn

    @pytest.fixture
    def key(self):
        if six.PY2:
            return 'tests.test_utils.<function fn '
        else:
            return 'tests.test_utils.<function TestCache.fn.<locals>.fn '

    def test_with_blank_cache(self, shelve, fn, key):
        assert shelve == {}
        assert fn() == 'test'
        assert shelve == {key: {'etag': '0', 'value': 'test'}}

    def test_with_filled_cache(self, shelve, fn, key):
        cache_value = {key: {'etag': '0', 'value': 'new-value'}}
        shelve.update(cache_value)
        assert fn() == 'new-value'
        assert shelve == cache_value

    def test_when_etag_changed(self, shelve, fn, key):
        shelve.update({key: {'etag': '-1', 'value': 'old-value'}})
        assert fn() == 'test'
        assert shelve == {key: {'etag': '0', 'value': 'test'}}


class TestCompatibilityCall(object):
    def test_match(self):
        def match(command):
            assert command == Command()
            return True

        assert compatibility_call(match, Command())

    def test_old_match(self, settings):
        def match(command, _settings):
            assert command == Command()
            assert settings == _settings
            return True

        with pytest.warns(UserWarning):
            assert compatibility_call(match, Command())

    def test_get_new_command(self):
        def get_new_command(command):
            assert command == Command()
            return True

        assert compatibility_call(get_new_command, Command())

    def test_old_get_new_command(self, settings):
        def get_new_command(command, _settings):
            assert command == Command()
            assert settings == _settings
            return True

        with pytest.warns(UserWarning):
            assert compatibility_call(get_new_command, Command())

    def test_side_effect(self):
        def side_effect(command, new_command):
            assert command == Command() == new_command
            return True

        assert compatibility_call(side_effect, Command(), Command())

    def test_old_side_effect(self, settings):
        def side_effect(command, new_command, _settings):
            assert command == Command() == new_command
            assert settings == _settings
            return True

        with pytest.warns(UserWarning):
            assert compatibility_call(side_effect, Command(), Command())


class TestGetValidHistoryWithoutCurrent(object):
    @pytest.yield_fixture(autouse=True)
    def fail_on_warning(self):
        warnings.simplefilter('error')
        yield
        warnings.resetwarnings()

    @pytest.fixture(autouse=True)
    def history(self, mocker):
        return mocker.patch('thefuck.shells.shell.get_history',
                            return_value=['le cat', 'fuck', 'ls cat',
                                          'diff x', 'nocommand x', u'café ô'])

    @pytest.fixture(autouse=True)
    def alias(self, mocker):
        return mocker.patch('thefuck.utils.get_alias',
                            return_value='fuck')

    @pytest.fixture(autouse=True)
    def bins(self, mocker, monkeypatch):
        monkeypatch.setattr('thefuck.conf.os.environ', {'PATH': 'path'})
        callables = list()
        for name in ['diff', 'ls', 'café']:
            bin_mock = mocker.Mock(name=name)
            bin_mock.configure_mock(name=name, is_dir=lambda: False)
            callables.append(bin_mock)
        path_mock = mocker.Mock(iterdir=mocker.Mock(return_value=callables))
        return mocker.patch('thefuck.utils.Path', return_value=path_mock)

    @pytest.mark.parametrize('script, result', [
        ('le cat', ['ls cat', 'diff x', u'café ô']),
        ('diff x', ['ls cat', u'café ô']),
        ('fuck', ['ls cat', 'diff x', u'café ô']),
        (u'cafe ô', ['ls cat', 'diff x', u'café ô']),
    ])
    def test_get_valid_history_without_current(self, script, result):
        command = Command(script=script)
        assert get_valid_history_without_current(command) == result
