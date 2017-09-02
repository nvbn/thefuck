import os
import pytest
import tarfile
from thefuck.rules.dirty_untar import match, get_new_command, side_effect, \
                                      tar_extensions  # noqa: E126
from thefuck.types import Command


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


parametrize_extensions = pytest.mark.parametrize('ext', tar_extensions)

# (filename as typed by the user, unquoted filename, quoted filename as per shells.quote)
parametrize_filename = pytest.mark.parametrize('filename, unquoted, quoted', [
    ('foo{}', 'foo{}', 'foo{}'),
    ('"foo bar{}"', 'foo bar{}', "'foo bar{}'")])

parametrize_script = pytest.mark.parametrize('script, fixed', [
    ('tar xvf {}', 'mkdir -p {dir} && tar xvf {filename} -C {dir}'),
    ('tar -xvf {}', 'mkdir -p {dir} && tar -xvf {filename} -C {dir}'),
    ('tar --extract -f {}', 'mkdir -p {dir} && tar --extract -f {filename} -C {dir}')])


@parametrize_extensions
@parametrize_filename
@parametrize_script
def test_match(ext, tar_error, filename, unquoted, quoted, script, fixed):
    tar_error(unquoted.format(ext))
    assert match(Command(script.format(filename.format(ext)), ''))


@parametrize_extensions
@parametrize_filename
@parametrize_script
def test_side_effect(ext, tar_error, filename, unquoted, quoted, script, fixed):
    tar_error(unquoted.format(ext))
    side_effect(Command(script.format(filename.format(ext)), ''), None)
    assert set(os.listdir('.')) == {unquoted.format(ext), 'd'}


@parametrize_extensions
@parametrize_filename
@parametrize_script
def test_get_new_command(ext, tar_error, filename, unquoted, quoted, script, fixed):
    tar_error(unquoted.format(ext))
    assert (get_new_command(Command(script.format(filename.format(ext)), ''))
            == fixed.format(dir=quoted.format(''), filename=filename.format(ext)))
