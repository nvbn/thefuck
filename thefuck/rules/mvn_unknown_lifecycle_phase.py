from thefuck import shells
from thefuck.utils import replace_command
from difflib import get_close_matches
import re


def match(command, settings):
    failedLifecycle = re.search('\[ERROR\] Unknown lifecycle phase "(.+)"', command.stdout)
    availableLifecycles = re.search('Available lifecycle phases are: (.+) -> \[Help 1\]', command.stdout)
    return availableLifecycles and failedLifecycle and command.script.startswith('mvn')


def get_new_command(command, settings):
    failedLifecycle = re.search('\[ERROR\] Unknown lifecycle phase "(.+)"', command.stdout)
    availableLifecycles = re.search('Available lifecycle phases are: (.+) -> \[Help 1\]', command.stdout)
    if availableLifecycles and failedLifecycle:
        selectedLifecycle = get_close_matches(failedLifecycle.group(1), availableLifecycles.group(1).split(", "), 3, 0.6)
        return replace_command(command, failedLifecycle.group(1), selectedLifecycle)
    else:
        return []
