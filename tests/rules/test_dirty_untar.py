import os
import pytest
import tarfile
from thefuck.rules.dirty_untar import match, get_new_command, side_effect
from tests.utils import Command


@pytest.fixture
def tar_error(tmpdir):
    def fixture(filename):
        path = os.path.join(str(tmpdir), filename)

        def reset(path):
            os.mkdir('d')
            with tarfile.TarFile(path, 'w') as archive:
                for file in ('a', 'b', 'c', 'd/e'):
                    with open(file, 'w') as f:
                        f.write('*')

                    archive.add(file)

                    os.remove(file)

            with tarfile.TarFile(path, 'r') as archive:
                archive.extractall()

        os.chdir(str(tmpdir))
        reset(path)

        assert set(os.listdir('.')) == {filename, 'a', 'b', 'c', 'd'}
        assert set(os.listdir('./d')) == {'e'}

    return fixture

parametrize_filename = pytest.mark.parametrize('filename', [
    'foo.tar',
    'foo.tar.gz',
    'foo.tgz'])

parametrize_script = pytest.mark.parametrize('script, fixed', [
    ('tar xvf {}', 'mkdir -p foo && tar xvf {} -C foo'),
    ('tar -xvf {}', 'mkdir -p foo && tar -xvf {} -C foo'),
    ('tar --extract -f {}', 'mkdir -p foo && tar --extract -f {} -C foo')])


@parametrize_filename
@parametrize_script
def test_match(tar_error, filename, script, fixed):
    tar_error(filename)
    assert match(Command(script=script.format(filename)))


@parametrize_filename
@parametrize_script
def test_side_effect(tar_error, filename, script, fixed):
    tar_error(filename)
    side_effect(Command(script=script.format(filename)), None)
    assert set(os.listdir('.')) == {filename, 'd'}


@parametrize_filename
@parametrize_script
def test_get_new_command(tar_error, filename, script, fixed):
    tar_error(filename)
    assert get_new_command(Command(script=script.format(filename))) == fixed.format(filename)
