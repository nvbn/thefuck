import pytest
from thefuck.specific.brew import brew_available, get_brew_path_prefix, all_brew_commands


@pytest.mark.fixtures('no_memoize')
def test_get_brew_path_prefix():
    assert get_brew_path_prefix() == "/usr/local" if brew_available else None


def test_all_brew_commands():
    assert all_brew_commands() == ['info', 'home', 'options', 'install', 'uninstall',
                                   'search', 'list', 'update', 'upgrade', 'pin', 'unpin',
                                   'doctor', 'create', 'edit'] if brew_available else None
