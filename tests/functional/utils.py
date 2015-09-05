import pytest
import os

enabled = os.environ.get('FUNCTIONAL')

functional = pytest.mark.skipif(
    not enabled,
    reason='Functional tests are disabled by default.')
