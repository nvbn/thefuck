import re
from thefuck.utils import for_app, replace_command
from thefuck.specific.npm import get_scripts, npm_available

enabled_by_default = npm_available


@for_app('npm')
def match(command):
    return (any(part.startswith('ru') for part in command.script_parts)
            and 'npm ERR! missing script: ' in command.output)


def get_new_command(command):
    misspelled_script = re.findall(
        r'.*missing script: (.*)\n', command.output)[0]
    return replace_command(command, misspelled_script, get_scripts())
