# -*- coding: utf-8 -*-

import os
import zipfile
from unicodedata import normalize

import pytest

from thefuck.rules.dirty_unzip import get_new_command, match, side_effect
from thefuck.types import Command


@pytest.fixture
def zip_error(tmpdir):
    def zip_error_inner(filename):
        path = os.path.join(str(tmpdir), filename)

        def reset(path):
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('a', '1')
                archive.writestr('b', '2')
                archive.writestr('c', '3')

                archive.writestr('d/e', '4')

                archive.extractall()

        os.chdir(str(tmpdir))
        reset(path)

        dir_list = os.listdir('.')
        if filename not in dir_list:
            filename = normalize('NFD', filename)

        assert set(dir_list) == {filename, 'a', 'b', 'c', 'd'}
        assert set(os.listdir('./d')) == {'e'}
    return zip_error_inner


@pytest.mark.parametrize('script,filename', [
    ('unzip café', 'café.zip'),
    ('unzip café.zip', 'café.zip'),
    ('unzip foo', 'foo.zip'),
    ('unzip foo.zip', 'foo.zip')])
def test_match(zip_error, script, filename):
    zip_error(filename)
    assert match(Command(script, ''))


@pytest.mark.parametrize('script,filename', [
    ('unzip café', 'café.zip'),
    ('unzip café.zip', 'café.zip'),
    ('unzip foo', 'foo.zip'),
    ('unzip foo.zip', 'foo.zip')])
def test_side_effect(zip_error, script, filename):
    zip_error(filename)
    side_effect(Command(script, ''), None)

    dir_list = os.listdir('.')
    if filename not in set(dir_list):
        filename = normalize('NFD', filename)

    assert set(dir_list) == {filename, 'd'}


@pytest.mark.parametrize('script,fixed,filename', [
    ('unzip café', "unzip café -d 'café'", 'café.zip'),
    ('unzip foo', 'unzip foo -d foo', 'foo.zip'),
    ("unzip 'foo bar.zip'", "unzip 'foo bar.zip' -d 'foo bar'", 'foo.zip'),
    ('unzip foo.zip', 'unzip foo.zip -d foo', 'foo.zip')])
def test_get_new_command(zip_error, script, fixed, filename):
    zip_error(filename)
    assert get_new_command(Command(script, '')) == fixed
