import subprocess
import itertools


def find_all_possible_commands(command):
    lower_command = command.script.lower().split()
    upper_command = command.script.upper().split()
    all_commands = []
    for i in lower_command:
        all_commands.append(i)
    for i in upper_command:
        all_commands.append(i)
    permutations = itertools.permutations(all_commands, len(lower_command))
    new_commands = []
    for per in permutations:
        new_command = ""
        for word in per:
            new_command += word + " "
        new_command = new_command.strip()
        if new_command not in new_commands:
            new_commands.append(new_command)
    return new_commands


def find_all_correct_commands(new_commands : list):
    all_correct_commands = []
    for com in new_commands:
        result = subprocess.getstatusoutput(com)
        if result[0] == 0:
            all_correct_commands.append(com)
    return all_correct_commands


def match(command):
    flag = False
    for i in command.script:
        if i.isupper():
            flag = True
    # checks if the command that typed is valid, if it is not it retunrs false
    # So if we type: SL -A (instead of LS -A) the rule will not be activated
    new_commands = find_all_possible_commands(command)
    all_correct_commands = find_all_correct_commands(new_commands)
    if len(all_correct_commands) == 0:
        flag = False
    return flag


def get_new_command(command):
    new_commands = find_all_possible_commands(command)
    all_correct_commands = find_all_correct_commands(new_commands)
    return all_correct_commands


priority = 900
