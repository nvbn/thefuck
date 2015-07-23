import re
import subprocess
from thefuck.utils import get_closest, replace_argument


def match(command, script):
    return command.script.startswith('gulp')\
        and 'is not in your gulpfile' in command.stdout


def get_gulp_tasks():
    proc = subprocess.Popen(['gulp', '--tasks-simple'],
                            stdout=subprocess.PIPE)
    return [line.decode('utf-8')[:-1]
            for line in proc.stdout.readlines()]


def get_new_command(command, script):
    wrong_task = re.findall(r"Task '(\w+)' is not in your gulpfile",
                            command.stdout)[0]
    fixed_task = get_closest(wrong_task, get_gulp_tasks())
    return replace_argument(command.script, wrong_task, fixed_task)
