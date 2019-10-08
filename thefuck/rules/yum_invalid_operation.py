from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app


@sudo_support
@for_app('yum')
def match(command):
    pass


def _get_operations():
    pass


@sudo_support
def get_new_command(command):
    pass
