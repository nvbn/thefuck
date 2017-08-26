from ..conf import settings
from . import read_log, rerun


def get_output(script, expanded):
    if settings.instant_mode:
        return read_log.get_output(script, expanded)
    else:
        return rerun.get_output(script, expanded)
