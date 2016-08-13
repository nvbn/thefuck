from io import BytesIO

import pytest
from thefuck.specific.npm import get_scripts

run_script_stdout = b'''
Lifecycle scripts included in code-view-web:
  test
    jest

available via `npm run-script`:
  build
    cp node_modules/ace-builds/src-min/ -a resources/ace/ && webpack --progress --colors -p --config ./webpack.production.config.js
  develop
    cp node_modules/ace-builds/src/ -a resources/ace/ && webpack-dev-server --progress --colors
  watch-test
    jest --verbose --watch

'''


@pytest.mark.usefixtures('no_memoize')
def test_get_scripts(mocker):
    patch = mocker.patch('thefuck.specific.npm.Popen')
    patch.return_value.stdout = BytesIO(run_script_stdout)
    assert get_scripts() == ['build', 'develop', 'watch-test']
