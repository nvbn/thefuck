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
    if subprocess.call(['docker', 'build', '--tag={}'.format(tag), tmpdir],
                       cwd=root) != 0:
        raise Exception("Can't build container")
    shutil.rmtree(tmpdir)


@contextmanager
def spawn(tag, dockerfile):
    build_container(tag, dockerfile)
    proc = pexpect.spawnu(
        'docker run --volume {}:/src --tty=true --interactive=true {}'.format(root, tag))
    proc.sendline('pip install /src')

    try:
        yield proc
    finally:
        proc.terminate()


functional = pytest.mark.skipif(
    not os.environ.get('FUNCTIONAL'),
    reason='Functional tests are disabled by default.')
