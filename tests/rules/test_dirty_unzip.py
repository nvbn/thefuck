# -*- coding: utf-8 -*-

import os
import pytest
import zipfile
from thefuck.rules.dirty_unzip import match, get_new_command, side_effect
from thefuck.types import Command
from unicodedata import normalize


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

        dir_list = os.listdir(u'.')
        if filename not in dir_list:
            filename = normalize('NFD', filename)

        assert set(dir_list) == {filename, 'a', 'b', 'c', 'd'}
        assert set(os.listdir('./d')) == {'e'}
    return zip_error_inner


@pytest.mark.parametrize('script,filename', [
    (u'unzip café', u'café.zip'),
    (u'unzip café.zip', u'café.zip'),
    (u'unzip foo', u'foo.zip'),
    (u'unzip foo.zip', u'foo.zip')])
def test_match(zip_error, script, filename):
    zip_error(filename)
    assert match(Command(script, ''))


@pytest.mark.parametrize('script,filename', [
    (u'unzip café', u'café.zip'),
    (u'unzip café.zip', u'café.zip'),
    (u'unzip foo', u'foo.zip'),
    (u'unzip foo.zip', u'foo.zip')])
def test_side_effect(zip_error, script, filename):
    zip_error(filename)
    side_effect(Command(script, ''), None)

    dir_list = os.listdir(u'.')
    if filename not in set(dir_list):
        filename = normalize('NFD', filename)

    assert set(dir_list) == {filename, 'd'}


@pytest.mark.parametrize('script,fixed,filename', [
    (u'unzip café', u"unzip café -d 'café'", u'café.zip'),
    (u'unzip foo', u'unzip foo -d foo', u'foo.zip'),
    (u"unzip 'foo bar.zip'", u"unzip 'foo bar.zip' -d 'foo bar'", u'foo.zip'),
    (u'unzip foo.zip', u'unzip foo.zip -d foo', u'foo.zip')])
def test_get_new_command(zip_error, script, fixed, filename):
    zip_error(filename)
    assert get_new_command(Command(script, '')) == fixed
