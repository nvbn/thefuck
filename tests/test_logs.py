from mock import Mock
from thefuck import logs


def test_color():
    assert logs.color('red', Mock(no_colors=False)) == 'red'
    assert logs.color('red', Mock(no_colors=True)) == ''


def test_debug(capsys):
    logs.debug('test', Mock(no_colors=True, debug=True))
    assert capsys.readouterr() == ('', 'DEBUG: test\n')
    logs.debug('test', Mock(no_colors=True, debug=False))
    assert capsys.readouterr() == ('', '')
