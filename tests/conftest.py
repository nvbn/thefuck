import pytest
from thefuck import shells
from thefuck import conf, const
from thefuck.system import Path

shells.shell = shells.Generic()


def pytest_addoption(parser):
    """Adds `--run-without-docker` argument."""
    group = parser.getgroup("thefuck")
    group.addoption('--enable-functional', action="store_true", default=False,
                    help="Enable functional tests")


@pytest.fixture
def no_memoize(monkeypatch):
    monkeypatch.setattr('thefuck.utils.memoize.disabled', True)


@pytest.fixture(autouse=True)
def settings(request):
    def _reset_settings():
        conf.settings.clear()
        conf.settings.update(const.DEFAULT_SETTINGS)

    request.addfinalizer(_reset_settings)
    conf.settings.user_dir = Path('~/.thefuck')
    return conf.settings


@pytest.fixture
def no_colors(settings):
    settings.no_colors = True


@pytest.fixture(autouse=True)
def no_cache(monkeypatch):
    monkeypatch.setattr('thefuck.utils.cache.disabled', True)


@pytest.fixture(autouse=True)
def functional(request):
    if request.node.get_marker('functional') \
            and not request.config.getoption('enable_functional'):
        pytest.skip('functional tests are disabled')


@pytest.fixture
def source_root():
    return Path(__file__).parent.parent.resolve()


@pytest.fixture
def set_shell(monkeypatch, request):
    def _set(cls):
        shell = cls()
        monkeypatch.setattr('thefuck.shells.shell', shell)
        request.addfinalizer()
        return shell

    return _set
