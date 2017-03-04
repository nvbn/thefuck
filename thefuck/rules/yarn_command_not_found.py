import re
from subprocess import Popen, PIPE
from thefuck.utils import for_app, eager, get_closest

regex = re.compile(r'error Command "(.*)" not found.')


@for_app('yarn')
def match(command):
    return regex.findall(command.stderr)


@eager
def _get_all_tasks():
    proc = Popen(['yarn', '--help'], stdout=PIPE)
    should_yield = False
    for line in proc.stdout.readlines():
        line = line.decode().strip()

        if 'Commands:' in line:
            should_yield = True
            continue

        if should_yield and '- ' in line:
            yield line.split(' ')[-1]


def get_new_command(command):
    misspelled_task = regex.findall(command.stderr)[0]
    tasks = _get_all_tasks()
    fixed = get_closest(misspelled_task, tasks)
    return command.script.replace(' {}'.format(misspelled_task),
                                  ' {}'.format(fixed))
