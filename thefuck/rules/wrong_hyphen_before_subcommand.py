from thefuck.utils import get_all_executables, get_close_matches, \
    get_valid_history_without_current, get_closest, which
from thefuck.specific.sudo import sudo_support
from thefuck import logs


import os.path
import subprocess
import gzip
import re


def get_manpage_dir():
    return "/usr/share/man"


def get_manpage_path(command, number = None):
    if number == None:
        return get_manpage_path(command, 1) or\
            get_manpage_path(command, 8) or\
            get_manpage_path(command, 7)
    
    path = os.path.join(get_manpage_dir(), "man%d" % (number,), "%s.%d.gz" % (command, number))
    return path if os.path.exists(path) else None


def get_manpage(command, number = None):
    path = get_manpage_path(command, number)
    if path:
        with gzip.open(path, "r") as f:
            return list(filter(None, (textify(line) for line in f.readlines())))
    else:
        return []


def textify(manline):
    manline = re.sub(r"^\.[A-Za-z]+( |$)", "", str(manline, "utf-8").strip()) # Stripping line headers .SH, .B
    manline = re.sub(r"\\f.", "", manline) # Stripping format
    manline = re.sub(r"\\(.)", r"\1", manline)
    return manline.replace('"', '').replace('\'', '')


def get_synopsis(man):
    try:
        return " ".join(line for line in man[man.index("SYNOPSIS") + 1: man.index("DESCRIPTION")])
    except ValueError:
        return []


def get_flags(man):
    return [x for x in man if x[0] == '-']


@sudo_support
def match(command):
    return False


@sudo_support
def get_new_command(command):
    return ""


priority = 1 # For debugging purposes only
