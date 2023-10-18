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

@pytest.fixture
def match_output(host):
    return cannot_resolve_output(host)

@pytest.mark.parametrize('script, host', [
    ('ping https://google.com', 'https://google.com'),
    ('ping http://google.com', 'http://google.com'),
    ('ping http://google.com/', 'http://google.com/'),
    ('ping http://google.com/?q=test', 'http://google.com/?q=test'),
    ('ping ftp://192.168.0.1', 'ftp://192.168.0.1'),
    ('ping -c 10 ftp://192.168.0.1', 'ftp://192.168.0.1'), # allow options at the beginning
    ('ping ftp://192.168.0.1 -c 10', 'ftp://192.168.0.1'), # allow options at the end
    ('ping -c 10 ftp://192.168.0.1 -t 10', 'ftp://192.168.0.1'), # allow options in between
])
def test_match(match_output, script, host):
    assert match(Command(script, match_output))

@pytest.fixture
def no_match_output(resolvable, host, ip):
    if resolvable:
        return resolve_output(host, ip, ip)
    else:
        return cannot_resolve_output(host)

@pytest.mark.parametrize('script, resolvable, host, ip', [
    ('ping http:/google.com/', False, 'http:/google.com/', None), # invalid url
    ('ping google.com', True, 'google.com', '142.250.70.174'),
    ('ping 127.0.0.1', True, '127.0.0.1', '127.0.0.1'),
    ('ping -c 10 google.com', True, 'google.com', '142.250.70.174'),
    ('ping google.com -c 10', True, 'google.com', '142.250.70.174'),
])
def test_not_match(no_match_output, script, resolvable, host, ip):
    assert not match(Command(script, no_match_output))


@pytest.mark.parametrize('new_command, script, host', [
    ('ping google.com', 'ping https://google.com', 'https://google.com'),
    ('ping -c 10 google.com', 'ping -c 10 https://google.com', 'https://google.com'),
    ('ping google.com -c 10', 'ping https://google.com -c 10', 'https://google.com'),
    ('ping -c 10 google.com -t 10', 'ping -c 10 https://google.com -t 10', 'https://google.com'),
])
def test_get_new_command(match_output, new_command, script, host):
    assert get_new_command(Command(script, match_output)) == new_command
