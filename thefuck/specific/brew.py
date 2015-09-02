import subprocess
from ..utils import memoize, which


enabled_by_default = bool(which('brew'))


@memoize
def get_brew_path_prefix():
    """To get brew path"""
    try:
        return subprocess.check_output(['brew', '--prefix'],
                                       universal_newlines=True).strip()
    except:
        return None
