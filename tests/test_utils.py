from contextlib import contextmanager
import pytest
from mock import Mock
from thefuck.utils import wrap_settings, \
    memoize, get_closest, get_all_executables, replace_argument, \
    get_all_matched_commands, is_app, for_app, cache
from thefuck.types import Settings
from tests.utils import Command


@pytest.mark.parametrize('override, old, new', [
    ({'key': 'val'}, {}, {'key': 'val'}),
    ({'key': 'new-val'}, {'key': 'val'}, {'key': 'val'}),
    ({'key': 'new-val', 'unset': 'unset'}, {'key': 'val'}, {'key': 'val', 'unset': 'unset'})])
def test_wrap_settings(override, old, new):
    fn = lambda _, settings: settings
    assert wrap_settings(override)(fn)(None, Settings(old)) == new


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
    def match(command, settings):
        return True

    assert match(Command(script), None) == result


class TestCache(object):
    @pytest.fixture(autouse=True)
    def enable_cache(self, monkeypatch):
        monkeypatch.setattr('thefuck.utils.cache.disabled', False)

    @pytest.fixture
    def shelve(self, mocker):
        value = {}

        @contextmanager
        def _shelve(path):
            yield value

        mocker.patch('thefuck.utils.shelve.open', new_callable=lambda: _shelve)
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

    def test_with_blank_cache(self, shelve, fn):
        assert shelve == {}
        assert fn() == 'test'
        assert shelve == {
            'tests.test_utils.<function TestCache.fn.<locals>.fn ': {
                'etag': '0', 'value': 'test'}}

    def test_with_filled_cache(self, shelve, fn):
        cache_value = {
            'tests.test_utils.<function TestCache.fn.<locals>.fn ': {
                'etag': '0', 'value': 'new-value'}}
        shelve.update(cache_value)
        assert fn() == 'new-value'
        assert shelve == cache_value

    def test_when_etag_changed(self, shelve, fn):
        shelve.update({
            'tests.test_utils.<function TestCache.fn.<locals>.fn ': {
                'etag': '-1', 'value': 'old-value'}})
        assert fn() == 'test'
        assert shelve == {
            'tests.test_utils.<function TestCache.fn.<locals>.fn ': {
                'etag': '0', 'value': 'test'}}
