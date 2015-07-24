import sys
import os
import pytest
from contextlib import contextmanager
import pexpect
import subprocess
import shutil
from tempfile import mkdtemp
from pathlib import Path

root = str(Path(__file__).parent.parent.parent.resolve())


def build_container(tag, dockerfile):
    tmpdir = mkdtemp()
    with Path(tmpdir).joinpath('Dockerfile').open('w') as file:
        file.write(dockerfile)
    if subprocess.call(['docker', 'build', '--tag={}'.format(tag), tmpdir]) != 0:
        raise Exception("Can't build container")
    shutil.rmtree(tmpdir)


def read_until(proc, string='\n$ '):
    text = ''
    while True:
        text += proc.read(1)
        sys.stdout.write(text[-1])
        sys.stdout.flush()
        if text.endswith(string):
            return text


def run(proc, cmd):
    proc.sendline(cmd)
    return read_until(proc)


@contextmanager
def spawn(tag, volume, prepare=None):
    if prepare is None:
        prepare = []

    proc = pexpect.spawnu(
        'docker run --volume {} --tty=true --interactive=true {}'.format(
            volume, tag))

    try:
        for line in prepare:
            run(proc, line)
        yield proc
    finally:
        proc.terminate()


functional = pytest.mark.skipif(
    not os.environ.get('FUNCTIONAL'),
    reason='Functional tests are disabled by default.')
