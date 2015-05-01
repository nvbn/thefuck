import os
import shelve
from tempfile import gettempdir
from psutil import Process


class History(object):
    """Temporary history of commands/fixed-commands dependent on
    current shell instance.

    """

    def __init__(self):
        self._path = os.path.join(gettempdir(), '.thefuck_history')
        self._pid = Process(os.getpid()).parent().pid
        self._db = shelve.open(self._path)

    def _prepare_key(self, key):
        return '{}-{}'.format(self._pid, key)

    def update(self, **kwargs):
        self._db.update({self._prepare_key(k): v for k,v in kwargs.items()})
        self._db.sync()
        return self

    def __getattr__(self, item):
        return self._db.get(self._prepare_key(item))
