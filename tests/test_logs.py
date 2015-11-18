import pytest
from thefuck import logs


def test_color(settings):
    settings.no_colors = False
    assert logs.color('red') == 'red'
    settings.no_colors = True
    assert logs.color('red') == ''


@pytest.mark.usefixtures('no_colors')
@pytest.mark.parametrize('debug, stderr', [
    (True, 'DEBUG: test\n'),
    (False, '')])
def test_debug(capsys, settings, debug, stderr):
    settings.debug = debug
    logs.debug('test')
    assert capsys.readouterr() == ('', stderr)
