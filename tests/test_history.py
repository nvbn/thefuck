import pytest
from mock import patch, Mock
from thefuck.history import History


@pytest.fixture
def process(monkeypatch):
    Process = Mock()
    Process.return_value.parent.return_value.pid = 1
    monkeypatch.setattr('thefuck.history.Process', Process)


@pytest.fixture
def db(monkeypatch):
    class DBMock(dict):
        def __init__(self):
            super(DBMock, self).__init__()
            self.sync = Mock()

        def __call__(self, *args, **kwargs):
            return self

    db = DBMock()
    monkeypatch.setattr('thefuck.history.shelve.open', db)
    return db


@pytest.mark.usefixtures('process')
class TestHistory(object):
    def test_set(self, db):
        history = History()
        history.update(last_script='ls',
                       last_fixed_script=None)
        assert db == {'1-last_script': 'ls',
                      '1-last_fixed_script': None}

    def test_get(self, db):
        history = History()
        db['1-last_script'] = 'cd ..'
        assert history.last_script == 'cd ..'

    def test_get_without_value(self, db):
        history = History()
        assert history.last_script is None
