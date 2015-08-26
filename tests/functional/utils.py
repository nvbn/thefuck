import pytest
import os
import subprocess
import shutil
from tempfile import mkdtemp
from pathlib import Path
import sys
import pexpect
from tests.utils import root


bare = os.environ.get('BARE')
enabled = os.environ.get('FUNCTIONAL')


def build_container(tag, dockerfile, copy_src=False):
    tmpdir = mkdtemp()
    try:
        if copy_src:
            subprocess.call(['cp', '-a', str(root), tmpdir])
        dockerfile_path = Path(tmpdir).joinpath('Dockerfile')
        with dockerfile_path.open('w') as file:
            file.write(dockerfile)
        if subprocess.call(['docker', 'build', '--tag={}'.format(tag), tmpdir]) != 0:
            raise Exception("Can't build a container")
    finally:
        shutil.rmtree(tmpdir)


def spawn(request, tag, dockerfile, cmd, install=True, copy_src=False):
    if bare:
        proc = pexpect.spawnu(cmd)
    else:
        tag = 'thefuck/{}'.format(tag)
        build_container(tag, dockerfile, copy_src)
        proc = pexpect.spawnu('docker run --volume {}:/src --tty=true '
                              '--interactive=true {} {}'.format(root, tag, cmd))
        if install:
            proc.sendline('pip install /src')

    proc.sendline('cd /')

    proc.logfile = sys.stdout

    request.addfinalizer(lambda: proc.terminate(True))
    return proc


def images(*items):
    if bare:
        return [items[0]]
    else:
        return items


functional = pytest.mark.skipif(
    not enabled,
    reason='Functional tests are disabled by default.')
