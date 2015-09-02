import pytest
from mock import Mock


@pytest.fixture
def no_memoize(monkeypatch):
    monkeypatch.setattr('thefuck.utils.memoize.disabled', True)


@pytest.fixture
def settings():
    return Mock(debug=False, no_colors=True)


@pytest.fixture(autouse=True)
def no_cache(monkeypatch):
    monkeypatch.setattr('thefuck.utils.cache.disabled', True)
