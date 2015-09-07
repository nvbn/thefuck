import os
import pytest
import zipfile
from thefuck.rules.dirty_unzip import match, get_new_command, side_effect
from tests.utils import Command


@pytest.fixture
def zip_error(tmpdir):
    path = os.path.join(str(tmpdir), 'foo.zip')

    def reset(path):
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('a', '1')
            archive.writestr('b', '2')
            archive.writestr('c', '3')

            archive.writestr('d/e', '4')

            archive.extractall()

    os.chdir(str(tmpdir))
    reset(path)

    assert set(os.listdir('.')) == {'foo.zip', 'a', 'b', 'c', 'd'}
    assert set(os.listdir('./d')) == {'e'}


@pytest.mark.parametrize('script', [
    'unzip foo',
    'unzip foo.zip'])
def test_match(zip_error, script):
    assert match(Command(script=script))


@pytest.mark.parametrize('script', [
    'unzip foo',
    'unzip foo.zip'])
def test_side_effect(zip_error, script):
    side_effect(Command(script=script), None)
    assert set(os.listdir('.')) == {'foo.zip', 'd'}


@pytest.mark.parametrize('script,fixed', [
    ('unzip foo', 'unzip foo -d foo'),
    ('unzip foo.zip', 'unzip foo.zip -d foo')])
def test_get_new_command(zip_error, script, fixed):
    assert get_new_command(Command(script=script)) == fixed
