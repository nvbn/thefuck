#!/usr/bin/env python
from subprocess import call
import os
import re


version = None


def get_new_setup_py_lines():
    global version
    with open('setup.py', 'r') as sf:
        current_setup = sf.readlines()
    for line in current_setup:
        if line.startswith('VERSION = '):
            major, minor = re.findall(r"VERSION = '(\d+)\.(\d+)'", line)[0]
            version = "{}.{}".format(major, int(minor) + 1)
            yield "VERSION = '{}'\n".format(version)
        else:
            yield line


lines = list(get_new_setup_py_lines())
with open('setup.py', 'w') as sf:
    sf.writelines(lines)

call('git pull', shell=True)
call('git commit -am "Bump to {}"'.format(version), shell=True)
call('git tag {}'.format(version), shell=True)
call('git push', shell=True)
call('git push --tags', shell=True)

env = os.environ
env['CONVERT_README'] = 'true'
call('python setup.py sdist bdist_wheel upload', shell=True, env=env)
