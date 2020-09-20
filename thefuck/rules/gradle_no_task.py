import re
from subprocess import Popen, PIPE
from thefuck.utils import for_app, eager, replace_command

regex = re.compile(r"Task '(.*)' (is ambiguous|not found)")


@for_app('gradle', 'gradlew')
def match(command):
    return regex.findall(command.output)


@eager
def _get_all_tasks(gradle):
    proc = Popen([gradle, 'tasks'], stdout=PIPE)
    should_yield = False
    for line in proc.stdout.readlines():
        line = line.decode().strip()
        if line.startswith('----'):
            should_yield = True
            continue

        if not line.strip():
            should_yield = False
            continue

        if should_yield and not line.startswith('All tasks runnable from root project'):
            yield line.split(' ')[0]


def get_new_command(command):
    wrong_task = regex.findall(command.output)[0][0]
    all_tasks = _get_all_tasks(command.script_parts[0])
    return replace_command(command, wrong_task, all_tasks)
