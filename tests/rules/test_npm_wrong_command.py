import pytest
from thefuck.rules.npm_wrong_command import match, get_new_command
from thefuck.types import Command

output = '''
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
    update, upgrade, v, verison, version, view, whoami

npm <cmd> -h     quick help on <cmd>
npm -l           display full usage info
npm faq          commonly asked questions
npm help <term>  search for help on <term>
npm help npm     involved overview

Specify configs in the ini-formatted file:
    /home/nvbn/.npmrc
or on the command line via: npm <command> --key value
Config info can be viewed via: npm help config

npm@2.14.7 /opt/node/lib/node_modules/npm
'''


@pytest.mark.parametrize('script', [
    'npm urgrdae',
    'npm urgrade -g',
    'npm -f urgrade -g',
    'npm urg'])
def test_match(script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('npm urgrade', ''),
    ('npm', output),
    ('test urgrade', output),
    ('npm -e', output)])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, result', [
    ('npm urgrade', 'npm upgrade'),
    ('npm -g isntall gulp', 'npm -g install gulp'),
    ('npm isntall -g gulp', 'npm install -g gulp')])
def test_get_new_command(script, result):
    assert get_new_command(Command(script, output)) == result
