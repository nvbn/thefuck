from thefuck.utils import get_all_executables
from thefuck.specific.sudo import sudo_support


import re
import gzip
import os.path
from functools import partial


def get_manpage_dir():
    """Returns the manpage directory for the system.

    :rtype: str

    Currently returns the default directory. On systems on which the manpage directory is configured
    otherwise, this rule will not function. TODO: Dynamically find the directory.
    """
    return "/usr/share/man"


def get_manpage_path(command, number=None):
    """Finds the specific manpage path inside the manpages directory for a given command.

    :type command: str
    :type number: int (optional, if not provided the number will be auto detected)
    :rtype: str (the path of the manpage for the command)
    """
    if number is None:
        return get_manpage_path(command, 1) or\
            get_manpage_path(command, 8) or\
            get_manpage_path(command, 7)

    path = os.path.join(get_manpage_dir(), "man%d" % (number,), "%s.%d.gz" % (command, number))
    return path if os.path.exists(path) else None


def get_manpage(command, number=None):
    """Returns the manpage for a command - a list of parsed lines

    :type command: str
    :type number: int (optional)
    :rtype: [str]
    """
    path = get_manpage_path(command, number)
    if path:
        with gzip.open(path, "r") as f:
            return list(filter(None, (textify(line) for line in f.readlines())))
    else:
        return []


def textify(manline):
    """Stringifies a manpage line (strips markdown instructions, unescapes characters and removes quotes)

    :type manline: bytes
    :rtype: str
    """
    # Stripping line headers .SH, .B
    manline = re.sub(r"^\.[A-Za-z]+( |$)", "", str(manline, "utf-8").strip())

    # Stripping format
    manline = re.sub(r"\\f.", "", manline)
    manline = re.sub(r"\\(.)", r"\1", manline)

    # Stripping quotes
    return manline.replace('"', '').replace('\'', '')


def get_synopsis(man):
    """Given a parsed manpage entry (as returned from get_manpage), returns the synopsis line from the manpage

    :type man: [str]
    :rtype: str
    """
    try:
        return " ".join(line for line in man[man.index("SYNOPSIS") + 1: man.index("DESCRIPTION")])
    except ValueError:
        return ""


def get_flags(man):
    """Given a parsed manpage entry (as returned from get_manpage), returns a list of lines which contain flag information

    :type man: [str]
    :rtype: [str]
    """
    return [x for x in man if x[0] == '-']


def find_at_start(word, line):
    return line.startswith(word) and\
        (len(line) == len(word) or line[len(word)] in ', (:')


def find_subcommand(manpage, command, subcommand):
    return any(map(partial(find_at_start, subcommand), manpage)) or\
        any(map(partial(find_at_start, "%s-%s" % (command, subcommand)), manpage))


def find_flag(flags, flag):
    return any(map(partial(find_at_start, '-' + flag), flags))


@sudo_support
def match(command):
    if command.script_parts[0] in get_all_executables():
        return False

    if '-' not in command.script_parts[0]:
        return False

    cmd, subcmd, *_ = command.script_parts[0].split('-')
    if cmd not in get_all_executables():
        return False

    manpage = get_manpage(cmd)
    if not manpage:
        return False

    synopsis = get_synopsis(manpage)
    if subcmd in synopsis:
        return True

    if find_subcommand(manpage, cmd, subcmd):
        return True

    flags = get_flags(manpage)
    for flag in subcmd:
        if not find_flag(flags, flag):
            return False

    return True


@sudo_support
def get_new_command(command):
    cmd, subcmd, *_ = command.script_parts[0].split('-')
    manpage = get_manpage(cmd)
    synopsis = get_synopsis(manpage)

    if subcmd in synopsis or find_subcommand(manpage, cmd, subcmd):
        # We are dealing with an accidentally added hyphen
        return command.script.replace('-', ' ', 1)

    else:
        # We are dealing with a missing space
        return command.script.replace('-', ' -', 1)


priority = 2500
