import pytest
from io import BytesIO
from tests.utils import Command
from thefuck.rules.npm_missing_script import match, get_new_command

stderr = '''
npm ERR! Linux 4.4.0-31-generic
npm ERR! argv "/opt/node/bin/node" "/opt/node/bin/npm" "run" "dvelop"
npm ERR! node v4.4.7
npm ERR! npm  v2.15.8

npm ERR! missing script: {}
npm ERR!
npm ERR! If you need help, you may report this error at:
npm ERR!     <https://github.com/npm/npm/issues>

npm ERR! Please include the following file with any support request:
npm ERR!     /home/nvbn/exp/code_view/client_web/npm-debug.log
'''.format

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


@pytest.fixture(autouse=True)
def run_script(mocker):
    patch = mocker.patch('thefuck.specific.npm.Popen')
    patch.return_value.stdout = BytesIO(run_script_stdout)
    return patch.return_value


@pytest.mark.parametrize('command', [
    Command('npm ru wach', stderr=stderr('wach')),
    Command('npm run live-tes', stderr=stderr('live-tes')),
    Command('npm run-script sahare', stderr=stderr('sahare'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('npm wach', stderr=stderr('wach')),
    Command('vim live-tes', stderr=stderr('live-tes')),
    Command('npm run-script sahare')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('script, stderr, result', [
    ('npm ru wach-tests', stderr('wach-tests'), 'npm ru watch-test'),
    ('npm -i run-script dvelop', stderr('dvelop'),
     'npm -i run-script develop'),
    ('npm -i run-script buld -X POST', stderr('buld'),
     'npm -i run-script build -X POST')])
def test_get_new_command(script, stderr, result):
    command = Command(script, stderr=stderr)

    assert get_new_command(command)[0] == result
