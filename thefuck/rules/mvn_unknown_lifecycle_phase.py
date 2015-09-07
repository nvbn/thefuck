from thefuck.utils import replace_command, for_app
from difflib import get_close_matches
import re


def _get_failed_lifecycle(command):
    return re.search(r'\[ERROR\] Unknown lifecycle phase "(.+)"',
                     command.stdout)


def _getavailable_lifecycles(command):
    return re.search(
        r'Available lifecycle phases are: (.+) -> \[Help 1\]', command.stdout)


@for_app('mvn')
def match(command):
    failed_lifecycle = _get_failed_lifecycle(command)
    available_lifecycles = _getavailable_lifecycles(command)
    return available_lifecycles and failed_lifecycle


def get_new_command(command):
    failed_lifecycle = _get_failed_lifecycle(command)
    available_lifecycles = _getavailable_lifecycles(command)
    if available_lifecycles and failed_lifecycle:
        selected_lifecycle = get_close_matches(
            failed_lifecycle.group(1), available_lifecycles.group(1).split(", "),
            3, 0.6)
        return replace_command(command, failed_lifecycle.group(1), selected_lifecycle)
    else:
        return []
