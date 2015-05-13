import pytest


@pytest.fixture(autouse=True)
def generic_shell(monkeypatch):
    monkeypatch.setattr('thefuck.shells.and_', lambda *x: ' && '.join(x))
