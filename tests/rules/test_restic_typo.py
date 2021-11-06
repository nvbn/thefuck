import pytest

from thefuck.rules.restic_typo import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def mistype_suggestion():
    return """
unknown command "snapshot" for "restic"

Did you mean this?
        snapshots
    """


def test_match(mistype_suggestion):
    assert match(Command('restic snapshot', mistype_suggestion))


def test_get_new_command(mistype_suggestion):
    assert (get_new_command(Command('restic snapshot', mistype_suggestion)) == ['restic snapshots'])
