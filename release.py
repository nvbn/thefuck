#!/usr/bin/env python
import os
import re
from subprocess import call

version = None


def get_new_setup_py_lines():
    global version
    with open('setup.py', 'r') as sf:
        current_setup = sf.readlines()
    for line in current_setup:
        if line.startswith('VERSION = '):
            major, minor = re.findall(r"VERSION = '(\d+)\.(\d+)'", line)[0]
            version = f"{major}.{int(minor) + 1}"
            yield f"VERSION = '{version}'\n"
        else:
            yield line


lines = list(get_new_setup_py_lines())
with open('setup.py', 'w') as sf:
    sf.writelines(lines)

call('git pull', shell=True)
call(f'git commit -am "Bump to {version}"', shell=True)
call(f'git tag {version}', shell=True)
call('git push', shell=True)
call('git push --tags', shell=True)

env = os.environ
env['CONVERT_README'] = 'true'
call('rm -rf dist/*', shell=True, env=env)
call('python setup.py sdist bdist_wheel', shell=True, env=env)
call('twine upload dist/*', shell=True, env=env)
