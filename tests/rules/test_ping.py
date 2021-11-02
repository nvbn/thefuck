import pytest
from thefuck.rules.ping import get_new_command, match
from thefuck.types import Command


cannot_resolve_output = '''
ping: cannot resolve {}: Unknown host
'''.format

resolve_output = '''
PING {} ({}): 56 data bytes
64 bytes from {}: icmp_seq=0 ttl=64 time=0.050 ms
'''.format

@pytest.mark.parametrize('command', [
    Command('ping https://google.com', cannot_resolve_output('https://google.com')),
    Command('ping http://google.com', cannot_resolve_output('http://google.com')),
    Command('ping http://google.com/', cannot_resolve_output('http://google.com/')),
    Command('ping http://google.com/?q=test', cannot_resolve_output('http://google.com/?q=test')),
    Command('ping ftp://192.168.0.1', cannot_resolve_output('ftp://192.168.0.1')),
    Command('ping -c 10 ftp://192.168.0.1', cannot_resolve_output('ftp://192.168.0.1')), # allow options
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('ping http:/google.com/', cannot_resolve_output('http:/google.com/')), # skip invalid url
    Command('ping google.com', resolve_output('google.com', '142.250.70.174', '142.250.70.174')),
    Command('ping 127.0.0.1', resolve_output('127.0.0.1', '127.0.0.1', '127.0.0.1')),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('ping https://google.com', cannot_resolve_output('https://google.com')), 'ping google.com'),
    (Command('ping -c 10 https://google.com', cannot_resolve_output('https://google.com')), 'ping -c 10 google.com'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
