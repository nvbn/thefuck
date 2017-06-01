#!/usr/bin/env python2
import subprocess
import re
from thefuck.corrector import get_corrected_command


enabled_by_default = True
priority = 100000


def list_aliases():

    aliases_list = subprocess.check_output(["bash", "-li", "-c", "alias"]).strip().split('\n')
    p = re.compile(r'^alias ')
    aliases_list = {re.sub(p, '', a).split("=")[0]: re.sub(p, '', a).split("=")[1] for a in aliases_list}
    return aliases_list


def match(command):

    return command in list_aliases()


def get_new_command(command):
    command = list_aliases()[command]
    return get_corrected_command(command)


if __name__ == "__main__":

    command = "gs"

    m = match(command)
    print(m)
    if m:
        print(get_new_command(command))

