import sys
import socket

from thefuck.logs import debug
from thefuck.const import SHELL_LOGGER_SOCKET_PATH


def match(command):
    return True


def get_new_command(command):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    list_of_commands = []
    try:
        sock.connect(SHELL_LOGGER_SOCKET_PATH)
        sock.send(command.script.encode())
        number_of_strings = int.from_bytes(sock.recv(1), sys.byteorder)
        for i in range(number_of_strings):
            length_of_string = int.from_bytes(sock.recv(1), sys.byteorder)
            list_of_commands.append(sock.recv(length_of_string).decode())
    finally:
        sock.close()
        return list_of_commands


# Make last priority
priority = 10000
