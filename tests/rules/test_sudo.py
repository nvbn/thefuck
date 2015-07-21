import pytest
from thefuck.rules.sudo import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('stderr, stdout', [
    ('Permission denied', ''),
    ('permission denied', ''),
    ("npm ERR! Error: EACCES, unlink", ''),
    ('requested operation requires superuser privilege', ''),
    ('need to be root', ''),
    ('need root', ''),
    ('must be root', ''),
    ('You don\'t have access to the history DB.', ''),
    ('', "error: [Errno 13] Permission denied: '/usr/local/lib/python2.7/dist-packages/ipaddr.py'")])
def test_match(stderr, stdout):
    assert match(Command(stderr=stderr, stdout=stdout), None)


def test_not_match():
    assert not match(Command(), None)


def test_get_new_command():
    assert get_new_command(Command('ls'), None) == 'sudo ls'
