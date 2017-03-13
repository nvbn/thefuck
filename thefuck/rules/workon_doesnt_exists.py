from thefuck.utils import for_app, replace_command, eager, memoize
from thefuck.system import Path


@memoize
@eager
def _get_all_environments():
    root = Path('~/.virtualenvs').expanduser()
    if not root.is_dir():
        return

    for child in root.iterdir():
        if child.is_dir():
            yield child.name


@for_app('workon')
def match(command):
    return (len(command.script_parts) >= 2
            and command.script_parts[1] not in _get_all_environments())


def get_new_command(command):
    misspelled_env = command.script_parts[1]
    create_new = u'mkvirtualenv {}'.format(misspelled_env)

    available = _get_all_environments()
    if available:
        return (replace_command(command, misspelled_env, available)
                + [create_new])
    else:
        return create_new
