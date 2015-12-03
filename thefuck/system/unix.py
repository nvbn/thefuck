import sys
import tty
import termios
import colorama
from .. import const

init_output = colorama.init


def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def get_key():
    ch = getch()

    if ch == '\x03':
        return const.KEY_CTRL_C
    elif ch == '\x1b':
        next_ch = getch()
        if next_ch == '[':
            last_ch = getch()

            if last_ch == 'A':
                return const.KEY_UP
            elif last_ch == 'B':
                return const.KEY_DOWN

    return ch
