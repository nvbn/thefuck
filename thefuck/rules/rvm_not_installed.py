import re
from thefuck.utils import for_app


@for_app('rvm')
def match(command):
    return (
        'is not installed' in command.output
        and 'rvm install' in command.output
    )


def get_new_command(command):
    # Extract the version from the rvm install suggestion in the output
    # e.g. To install do: 'rvm install "ruby-2.7.2"'
    install_match = re.search(r"rvm install ['\"]?(ruby-[\d.]+)['\"]?", command.output)
    if install_match:
        return 'rvm install {}'.format(install_match.group(1))
    # Fallback: suggest rvm install with the version from the original command
    return 'rvm install ruby-{}'.format(' '.join(command.script_parts[2:]))
