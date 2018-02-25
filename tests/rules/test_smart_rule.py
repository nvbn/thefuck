import pytest
from mock import patch, MagicMock
from thefuck.rules.smart_rule import match, get_new_command


def test_match_simple():
    assert match('')


@pytest.mark.parametrize('script, socket_response, new_command', [
    ('git push', [b'\x03', b'\x25', b'git push --set-upstream origin master', b'\x16',
                  b'git push origin master', b'\x17', b'git push origin develop'],
     ['git push --set-upstream origin master', 'git push origin master', 'git push origin develop']),
    ('ls', [b'\x01', b'\x06', b'ls -la'], ['ls -la'])
])
@patch('thefuck.rules.smart_rule.socket')
def test_get_new_command(socket_mock, script, socket_response, new_command):
    sock_mock = MagicMock()
    recv_mock = MagicMock(side_effect=socket_response)
    socket_mock.socket.return_value = sock_mock
    sock_mock.recv = recv_mock
    returned_commands = get_new_command(script)
    assert returned_commands == new_command


@patch('thefuck.rules.smart_rule.socket')
def test_socket_open_close_connect(socket_mock):
    sock_mock = MagicMock()
    socket_mock.socket.return_value = sock_mock
    get_new_command('')
    socket_mock.socket.assert_called_once()
    sock_mock.connect.assert_called_once()
    sock_mock.close.assert_called_once()
