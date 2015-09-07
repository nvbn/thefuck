import pytest
from thefuck import conf


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
    request.addfinalizer(lambda: conf.settings.update(conf.DEFAULT_SETTINGS))
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
