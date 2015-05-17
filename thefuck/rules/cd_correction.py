#!/usr/bin/env python
__author__ = "mmussomele"

"""Attempts to spellcheck and correct failed cd commands"""

import os
import cd_mkdir
from thefuck.utils import sudo_support

MAX_ALLOWED_STR_DIST = 5

def _get_sub_dirs(parent):
    """Returns a list of the child directories of the given parent directory"""
    return [child for child in os.listdir(parent) if os.path.isdir(os.path.join(parent, child))]

def _dam_lev_dist():
    """Returns a Damerau-Levenshtein distance calculator."""
    cache = {}
    def _calculator(first, second):
        """
        Calculates the Damerau-Levenshtein distance of two strings.
        See: http://en.wikipedia.org/wiki/Damerau-Levenshtein_distance#Algorithm
        """
        if (first, second) in cache:
            return cache[(first, second)]
        else:
            l_first = len(first)
            l_second = len(second)
            distances = [[0 for _ in range(l_second + 1)] for _ in range(l_first + 1)]
            for i in range(l_first + 1):
                distances[i][0] = i
            for j in range(1, l_second + 1):
                distances[0][j] = j
            for i in range(l_first):
                for j in range(l_second):
                    if first[i] == second[j]:
                        cost = 0
                    else:
                        cost = 1
                    distances[i+1][j+1] = min(distances[i][j+1] + 1, 
                                              distances[i+1][j] + 1,
                                              distances[i][j] + cost)
                    if i and j and first[i] == second[j-1] and first[i-1] == second[j]:
                        distances[i][j] = min(distances[i+1][j+1],
                                              distances[i-1][j-1] + cost)
            cache[(first, second)] = distances[l_first][l_second]
            return distances[l_first][l_second]
    return _calculator

_dam_lev_dist = _dam_lev_dist()

@sudo_support
def match(command, settings):
    """Match function copied from cd_mkdir.py"""
    return (command.script.startswith('cd ')
        and ('no such file or directory' in command.stderr.lower()
            or 'cd: can\'t cd to' in command.stderr.lower()))

@sudo_support
def get_new_command(command, settings):
    """
    Attempt to rebuild the path string by spellchecking the directories.
    If it fails (i.e. no directories are a close enough match), then it 
    defaults to the rules of cd_mkdir. 
    Change sensitivity to matching by changing MAX_ALLOWED_STR_DIST. 
    Higher values allow for larger discrepancies in path names. 
    """
    dest = command.script.split()[1].split(os.sep)
    if dest[-1] == '':
        dest = dest[:-1]
    cwd = os.getcwd()
    for directory in dest:
        if directory == ".":
            continue
        elif directory == "..":
            cwd = os.path.split(cwd)[0]
            continue
        best_match = min(_get_sub_dirs(cwd), key=lambda x: _dam_lev_dist(directory, x))
        if _dam_lev_dist(directory, best_match) > MAX_ALLOWED_STR_DIST:
            return cd_mkdir.get_new_command(command, settings)
        else:
            cwd = os.path.join(cwd, best_match)
    return "cd {0}".format(cwd) 

enabled_by_default = True
