import pytest
from io import BytesIO
from thefuck.rules.npm_run_script import match, get_new_command
from tests.utils import Command

stdout = '''
Usage: npm <command>

where <command> is one of:
    access, add-user, adduser, apihelp, author, bin, bugs, c,
    cache, completion, config, ddp, dedupe, deprecate, dist-tag,
    dist-tags, docs, edit, explore, faq, find, find-dupes, get,
    help, help-search, home, i, info, init, install, issues, la,
    link, list, ll, ln, login, logout, ls, outdated, owner,
    pack, ping, prefix, prune, publish, r, rb, rebuild, remove,
    repo, restart, rm, root, run-script, s, se, search, set,
    show, shrinkwrap, star, stars, start, stop, t, tag, team,
    test, tst, un, uninstall, unlink, unpublish, unstar, up,
    update, upgrade, v, version, view, whoami

npm <cmd> -h     quick help on <cmd>
npm -l           display full usage info
npm faq          commonly asked questions
npm help <term>  search for help on <term>
npm help npm     involved overview

Specify configs in the ini-formatted file:
    /home/nvbn/.npmrc
or on the command line via: npm <command> --key value
Config info can be viewed via: npm help config

'''

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


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('script', [
    'npm watch-test', 'npm develop'])
def test_match(script):
    command = Command(script, stdout)
    assert match(command)


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('command, run_script_out', [
    (Command('npm test', 'TEST FAIL'), run_script_stdout),
    (Command('npm watch-test', 'TEST FAIL'), run_script_stdout),
    (Command('npm test', stdout), run_script_stdout),
    (Command('vim watch-test', stdout), run_script_stdout)])
def test_not_match(run_script, command, run_script_out):
    run_script.stdout = BytesIO(run_script_out)
    assert not match(command)


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('script, result', [
    ('npm watch-test', 'npm run-script watch-test'),
    ('npm -i develop', 'npm run-script -i develop'),
    ('npm -i watch-script --path ..',
     'npm run-script -i watch-script --path ..')])
def test_get_new_command(script, result):
    command = Command(script, stdout)
    assert get_new_command(command) == result
