from mock import Mock
from thefuck import logs


def test_color():
    assert logs.color('red', Mock(no_colors=False)) == 'red'
    assert logs.color('red', Mock(no_colors=True)) == ''
