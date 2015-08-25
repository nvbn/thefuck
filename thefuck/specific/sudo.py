from functools import wraps
import six
from ..types import Command


def sudo_support(fn):
    """Removes sudo before calling fn and adds it after."""
    @wraps(fn)
    def wrapper(command, settings):
        if not command.script.startswith('sudo '):
            return fn(command, settings)

        result = fn(Command(command.script[5:],
                            command.stdout,
                            command.stderr),
                    settings)

        if result and isinstance(result, six.string_types):
            return u'sudo {}'.format(result)
        elif isinstance(result, list):
            return [u'sudo {}'.format(x) for x in result]
        else:
            return result
    return wrapper