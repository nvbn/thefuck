import six
from decorator import decorator
from ..types import Command


@decorator
def sudo_support(fn, command, settings):
    """Removes sudo before calling fn and adds it after."""
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
