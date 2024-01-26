from mock import Mock
import pytest
from thefuck.entrypoints.alias import _get_alias, print_alias


@pytest.mark.parametrize(
    'py2, enable_experimental_instant_mode, which, is_instant',
    [
        (False, True, True, True),
        (False, False, True, False),
        (False, True, False, False),
        (True, True, True, False),
        (True, True, False, False),
        (True, False, True, False)
    ]
)
def test_get_alias(monkeypatch, mocker, py2,
                   enable_experimental_instant_mode,
                   which, is_instant):
    monkeypatch.setattr('six.PY2', py2)
    args = Mock(
        enable_experimental_instant_mode=enable_experimental_instant_mode,
        alias='fuck',
    )
    mocker.patch('thefuck.entrypoints.alias.which', return_value=which)
    shell = Mock(
        app_alias=lambda _: 'app_alias',
        instant_mode_alias=lambda _: 'instant_mode_alias'
    )
    monkeypatch.setattr('thefuck.entrypoints.alias.shell', shell)

    alias = _get_alias(args)
    if is_instant:
        assert alias == 'instant_mode_alias'
    else:
        assert alias == 'app_alias'


def test_print_alias(mocker):
    settings_mock = mocker.patch('thefuck.entrypoints.alias.settings')
    _get_alias_mock = mocker.patch('thefuck.entrypoints.alias._get_alias')
    known_args = Mock()
    print_alias(known_args)
    settings_mock.init.assert_called_once_with(known_args)
    _get_alias_mock.assert_called_once_with(known_args)
