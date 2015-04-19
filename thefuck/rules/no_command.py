from subprocess import Popen, PIPE
import re
from thefuck.utils import which, wrap_settings

local_settings = {'command_not_found': '/usr/lib/command-not-found'}


def _get_output(command, settings):
    name = command.script.split(' ')[command.script.startswith('sudo')]
    check_script = '{} {}'.format(settings.command_not_found, name)
    result = Popen(check_script, shell=True, stderr=PIPE)
    return result.stderr.read().decode('utf-8')

def _count_history_uses(name):
    script = "history | egrep '\\b{}\\b' | wc -l".format(name)
    result = Popen(script, shell=True,
                   stdout=PIPE)
    return int(result.stdout.read())

def _get_candidate_commands(command, settings):
    output = _get_output(command, settings)
    if "No command" in output and "from package" in output:
        fixed_names = re.findall(r"Command '([^']*)' from package",
                            output)
        return [name for name in fixed_names if which(name)]
    return []
        


@wrap_settings(local_settings)
def match(command, settings):
    if which(settings.command_not_found):
        output = _get_output(command, settings)
        return len(_get_candidate_commands(command, settings)) != 0



@wrap_settings(local_settings)
def get_new_command(command, settings):
    output = _get_output(command, settings)
    broken_name = re.findall(r"No command '([^']*)' found",
                             output)[0]
    candidates = _get_candidate_commands(command, settings)
    fixed_name = sorted(candidates, key=_count_history_uses, reverse=True)[0]
    return command.script.replace(broken_name, fixed_name)
     
