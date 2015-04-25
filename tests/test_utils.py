from mock import Mock
from thefuck.utils import sudo_support, wrap_settings
from thefuck.types import Settings
from tests.utils import Command


def test_wrap_settings():
    fn = lambda _, settings: settings
    assert wrap_settings({'key': 'val'})(fn)(None, Settings({})) \
           == {'key': 'val'}
    assert wrap_settings({'key': 'new-val'})(fn)(
        None, Settings({'key': 'val'})) == {'key': 'new-val'}


def test_sudo_support():
    fn = Mock(return_value=True, __name__='')
    assert sudo_support(fn)(Command('sudo ls'), None)
    fn.assert_called_once_with(Command('ls'), None)

    fn.return_value = False
    assert not sudo_support(fn)(Command('sudo ls'), None)

    fn.return_value = 'pwd'
    assert sudo_support(fn)(Command('sudo ls'), None) == 'sudo pwd'

    assert sudo_support(fn)(Command('ls'), None) == 'pwd'
