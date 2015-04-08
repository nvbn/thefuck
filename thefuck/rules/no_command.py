from subprocess import Popen, PIPE
import re


def _get_output(command):
    name = command.script.split(' ')[command.script.startswith('sudo')]
    check_script = '/usr/lib/command-not-found {}'.format(name)
    result = Popen(check_script, shell=True, stderr=PIPE)
    return result.stderr.read().decode()


def match(command):
    output = _get_output(command)
    return "No command" in output and "from package" in output


def get_new_command(command):
    output = _get_output(command)
    broken_name = re.findall(r"No command '([^']*)' found",
                             output)[0]
    fixed_name = re.findall(r"Command '([^']*)' from package",
                            output)[0]
    return command.script.replace(broken_name, fixed_name)
