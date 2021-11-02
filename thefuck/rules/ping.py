# -*- encoding: utf-8 -*-
from six.moves.urllib.parse import urlparse
from thefuck.utils import for_app


@for_app('ping')
def match(command):
    # It only fix if the target host is a valid url
    try:
        results = urlparse(command.script_parts[-1])
        is_valid_url = results.hostname is not None
    except Exception:
        is_valid_url = False
    return 'cannot resolve' in command.output and is_valid_url


def get_new_command(command):
    result = urlparse(command.script_parts[-1])
    return ' '.join(command.script_parts[:-1]) + ' ' + result.hostname
