import re
from subprocess import PIPE, Popen

from thefuck.utils import cache, eager, for_app, get_closest

regex = re.compile(r'Warning: Task "(.*)" not found.')


@for_app('grunt')
def match(command):
    return regex.findall(command.output)


@cache('Gruntfile.js')
@eager
def _get_all_tasks():
    proc = Popen(['grunt', '--help'], stdout=PIPE)
    should_yield = False
    for line in proc.stdout.readlines():
        line = line.decode().strip()

        if 'Available tasks' in line:
            should_yield = True
            continue

        if should_yield and not line:
            return

        if '  ' in line:
            yield line.split(' ')[0]


def get_new_command(command):
    misspelled_task = regex.findall(command.output)[0].split(':')[0]
    tasks = _get_all_tasks()
    fixed = get_closest(misspelled_task, tasks)
    return command.script.replace(f' {misspelled_task}',
                                  f' {fixed}')
