import sys
import socket

from thefuck.conf import settings
from thefuck.const import SHELL_LOGGER_SOCKET_PATH


def match(command):
    import ipdb; ipdb.set_trace()
    return True


def get_new_command(command):
    import ipdb; ipdb.set_trace()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    list_of_commands = []
    try:
        sock.connect(settings.env.get(SHELL_LOGGER_SOCKET_PATH))
        sock.sendall(command)
        number_of_strings = int.from_bytes(sock.recv(1), sys.byteorder)
        for i in range(number_of_strings):
            length_of_string = int.from_bytes(sock.recv(1), sys.byteorder)
            list_of_commands.append(sock.recv(length_of_string).decode('utf-8'))
    finally:
        sock.close()
        return list_of_commands


# Make last priority
priority = 10000
