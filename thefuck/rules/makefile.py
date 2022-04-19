import os
from os.path import isfile, join
from thefuck.utils import get_closest

TOLERANCE = 0.6
COMMON_MISSPELLINGS = ['mke', 'maek', 'amke', 'meak', 'mkae', 'ake', 'mae', 'mak', 'makee', 'mmake', 'nake', 'makr', 'mske']

def makefile_in_directory():
    """
    Returns the name of the Makefile in the current directory.
    Will return a blank string if no makefile found.
    """
    name_of_makefile = ""
    file_list = [f for f in os.listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
    if 'GNUmakefile' in file_list:
        name_of_makefile = 'GNUmakefile'
    elif 'makefile' in file_list:
        name_of_makefile = 'makefile'
    elif 'Makefile' in file_list:
        name_of_makefile = 'Makefile'
    return name_of_makefile

def match(command):
    """Match function that determines if this rule could fix this command"""
    if len(makefile_in_directory()) == 0:
        # This would mean there is no makefile in the directory, we do not have a match
        return False
    first_word = command.script_parts[0].lower()
    if first_word in COMMON_MISSPELLINGS:
        # There is a Makefile and the first word of the command was a misspelling of 'make'
        return True
    if 'no rule to make target' in command.output.lower():
        # The target passed into the make command was misspelled or did not exist
        return True
    return False


def get_new_command(command):
    """
    Attempt to rebuild the make command by spellchecking the targets.
    If it fails (i.e. no targets are a close enough match), then it
    defaults to first make target in the file.
    Change sensitivity by changing TOLERANCE. Default value is 0.6
    """
    # Get possible targets from makefile and find the most similar.
    name_of_makefile = makefile_in_directory()
    possible_targets = []
    with open(name_of_makefile, 'r') as openfile:
        lines = openfile.readlines()
        for line in lines: # Loop through the makefile lines and find all targets
            line = line.strip()
            parts = line.split(':')
            if len(parts) > 1: # If there is a colon
                if parts[0][0] != '.': # If it is a valid target
                    possible_targets.append(parts[0])
    new_target = get_closest(' '.join(command.script_parts[1:]), possible_targets, cutoff=TOLERANCE)
    return "make " + new_target



    