from thefuck.utils import get_all_executables, get_close_matches, \
    get_valid_history_without_current, get_closest, which
from thefuck.specific.sudo import sudo_support
from thefuck import logs

import os.path
import subprocess
import gzip

def get_manpage_dir():
    return "/usr/share/man"


def get_manpage_path(command, number = None):
    if number == None:
        return get_manpage_path(command, 1) or
            get_manpage_path(command, 8) or
            get_manpage_path(command, 7)
    
    path = os.path.join(get_manpage_dir(), "man%d" % (number,), "%s.%d.gz" % (command, number))
    return path if os.path.exists(path) else None


def get_manpage(command, number = None):
    path = get_manpage_path(command, number)
    if path:
        with gzip.open(path, "r") as f:
            return [line.strip() for line in f.readlines()]
    else:
        return []


@sudo_support
def match(command):
    return False


@sudo_support
def get_new_command(command):
    return ""


priority = 1 # For debugging purposes only
