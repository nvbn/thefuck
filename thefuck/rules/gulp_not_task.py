import re
import subprocess
from thefuck.utils import replace_command, for_app


@for_app('gulp')
def match(command):
    return 'is not in your gulpfile' in command.stdout


def get_gulp_tasks():
    proc = subprocess.Popen(['gulp', '--tasks-simple'],
                            stdout=subprocess.PIPE)
    return [line.decode('utf-8')[:-1]
            for line in proc.stdout.readlines()]


def get_new_command(command):
    wrong_task = re.findall(r"Task '(\w+)' is not in your gulpfile",
                            command.stdout)[0]
    return replace_command(command, wrong_task, get_gulp_tasks())
