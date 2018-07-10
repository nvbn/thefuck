import errno
import gettext
import os
import warnings

import pytest

from thefuck.rules.cat_dir import match, get_new_command
from thefuck.types import Command

# patch this so the libc locale is available in the testing virtualenv
gettext._default_localedir = '/usr/share/locale'

lang_vars = ['LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG']


@pytest.fixture(params=['en_US.UTF-8', 'fr_FR.UTF-8', 'en_US.ISO8859-1', 'fr_FR.ISO8859-1'])
def language(request):
    return request.param


@pytest.fixture(params=[''] + lang_vars)
def environment(request, language):
    orig_env = os.environ.copy()

    # empty the locale environment variables
    for lang_var in lang_vars:
        os.environ.pop(lang_var, None)

    if request.param:
        os.environ[request.param] = language

    yield

    os.environ = orig_env


@pytest.fixture
def eisdir(environment):
    eisdir = gettext.translation('libc', fallback=True).gettext('Is a directory')
    return eisdir


@pytest.fixture(params=['foo', '/foo/var', 'cat/'])
def cat_command(request, eisdir):
    return (
        Command('cat %s' % request.param, 'cat: %s: %s\n' % (request.param, eisdir)),
        'ls %s' % request.param
    )


def test_localization_possible(language):
    if not language.startswith('en_US'):
        try:
            gettext.translation('libc', languages=[language])
        except EnvironmentError as e:
            if e.errno == errno.ENOENT:
                warnings.warn("No '%s' translation file found for language '%s'; the localization tests for `cat_dir` will be ineffective" % (e.filename, language))
            else:
                raise


def test_match(cat_command):
    assert match(cat_command[0])


@pytest.mark.parametrize('command', [
    Command('cat foo', 'foo bar baz'),
    Command('cat foo bar', 'foo bar baz'),
])
def test_not_match(command):
    assert not match(command)


def test_get_new_command(cat_command):
    assert get_new_command(cat_command[0]) == cat_command[1]
