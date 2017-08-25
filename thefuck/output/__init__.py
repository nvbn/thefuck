from ..conf import settings
from . import read_log, rerun


def get_output(script):
    if settings.instant_mode:
        return read_log.get_output(script)
    else:
        return rerun.get_output(script)
