"""Attempts to spellcheck and correct failed cd commands"""

import os
import six
from difflib import get_close_matches
from thefuck.specific.sudo import sudo_support
from thefuck.rules import cd_mkdir
from thefuck.utils import for_app

__author__ = "mmussomele"

MAX_ALLOWED_DIFF = 0.6


def _get_sub_dirs(parent):
    """Returns a list of the child directories of the given parent directory"""
    return [child for child in os.listdir(parent) if os.path.isdir(os.path.join(parent, child))]


@sudo_support
@for_app('cd')
def match(command):
    """Match function copied from cd_mkdir.py"""
    return (command.script.startswith('cd ')
            and ('no such file or directory' in command.stderr.lower()
                 or 'cd: can\'t cd to' in command.stderr.lower()))


@sudo_support
def get_new_command(command):
    """
    Attempt to rebuild the path string by spellchecking the directories.
    If it fails (i.e. no directories are a close enough match), then it
    defaults to the rules of cd_mkdir.
    Change sensitivity by changing MAX_ALLOWED_DIFF. Default value is 0.6
    """
    dest = command.script_parts[1].split(os.sep)
    if dest[-1] == '':
        dest = dest[:-1]
    if six.PY2:
        cwd = os.getcwdu()
    else:
        cwd = os.getcwd()
    for directory in dest:
        if directory == ".":
            continue
        elif directory == "..":
            cwd = os.path.split(cwd)[0]
            continue
        best_matches = get_close_matches(directory, _get_sub_dirs(cwd), cutoff=MAX_ALLOWED_DIFF)
        if best_matches:
            cwd = os.path.join(cwd, best_matches[0])
        else:
            return cd_mkdir.get_new_command(command)
    return u'cd "{0}"'.format(cwd)


enabled_by_default = True
