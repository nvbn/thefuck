from ..conf import settings
from . import read_log, rerun


def get_output(script, expanded):
    """Get output of the script.

    :param script: Console script.
    :type script: str
    :param expanded: Console script with expanded aliases.
    :type expanded: str
    :rtype: str

    """
    if settings.instant_mode:
        return read_log.get_output(script)
    else:
        return rerun.get_output(script, expanded)
