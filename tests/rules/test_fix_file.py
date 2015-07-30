import pytest
import os
from thefuck.rules.fix_file import match, get_new_command
from tests.utils import Command


# (script, file, line, col (or None), stderr)
tests = (
('gcc a.c', 'a.c', 3, 1,
"""
a.c: In function 'main':
a.c:3:1: error: expected expression before '}' token
 }
  ^
"""),

('clang a.c', 'a.c', 3, 1,
"""
a.c:3:1: error: expected expression
}
^
"""),

('perl a.pl', 'a.pl', 3, None,
"""
syntax error at a.pl line 3, at EOF
Execution of a.pl aborted due to compilation errors.
"""),

('perl a.pl', 'a.pl', 2, None,
"""
Search pattern not terminated at a.pl line 2.
"""),

('sh a.sh', 'a.sh', 2, None,
"""
a.sh: line 2: foo: command not found
"""),

('zsh a.sh', 'a.sh', 2, None,
"""
a.sh:2: command not found: foo
"""),

('bash a.sh', 'a.sh', 2, None,
"""
a.sh: line 2: foo: command not found
"""),

('rustc a.rs', 'a.rs', 2, 5,
"""
a.rs:2:5: 2:6 error: unexpected token: `+`
a.rs:2     +
           ^
"""),

('cargo build', 'src/lib.rs', 3, 5,
"""
   Compiling test v0.1.0 (file:///tmp/fix-error/test)
   src/lib.rs:3:5: 3:6 error: unexpected token: `+`
   src/lib.rs:3     +
                    ^
Could not compile `test`.

To learn more, run the command again with --verbose.
"""),

('python a.py', 'a.py', 2, None,
"""
  File "a.py", line 2
      +
          ^
SyntaxError: invalid syntax
"""),

('python a.py', 'a.py', 8, None,
"""
Traceback (most recent call last):
  File "a.py", line 8, in <module>
    match("foo")
  File "a.py", line 5, in match
    m = re.search(None, command)
  File "/usr/lib/python3.4/re.py", line 170, in search
    return _compile(pattern, flags).search(string)
  File "/usr/lib/python3.4/re.py", line 293, in _compile
    raise TypeError("first argument must be string or compiled pattern")
TypeError: first argument must be string or compiled pattern
"""
),

('ruby a.rb', 'a.rb', 3, None,
"""
a.rb:3: syntax error, unexpected keyword_end
"""),

('lua a.lua', 'a.lua', 2, None,
"""
lua: a.lua:2: unexpected symbol near '+'
"""),

('fish a.sh', '/tmp/fix-error/a.sh', 2, None,
"""
fish: Unknown command 'foo'
/tmp/fix-error/a.sh (line 2): foo
                              ^
"""),

('./a', './a', 2, None,
"""
awk: ./a:2: BEGIN { print "Hello, world!" + }
awk: ./a:2:                                 ^ syntax error
"""),

('llc a.ll', 'a.ll', 1, None,
"""
llc: a.ll:1:1: error: expected top-level entity
+
^
"""),

('go build a.go', 'a.go', 1, None,
"""
can't load package:
a.go:1:1: expected 'package', found '+'
"""),

('make', 'Makefile', 2, None,
"""
bidule
make: bidule: Command not found
Makefile:2: recipe for target 'target' failed
make: *** [target] Error 127
"""),

('git st', '/home/martin/.config/git/config', 1, None,
"""
fatal: bad config file line 1 in /home/martin/.config/git/config
"""),

('node fuck.js asdf qwer', '/Users/pablo/Workspace/barebones/fuck.js', '2', 5,
"""
/Users/pablo/Workspace/barebones/fuck.js:2
conole.log(arg);  // this should read console.log(arg);
^
ReferenceError: conole is not defined
    at /Users/pablo/Workspace/barebones/fuck.js:2:5
    at Array.forEach (native)
    at Object.<anonymous> (/Users/pablo/Workspace/barebones/fuck.js:1:85)
    at Module._compile (module.js:460:26)
    at Object.Module._extensions..js (module.js:478:10)
    at Module.load (module.js:355:32)
    at Function.Module._load (module.js:310:12)
    at Function.Module.runMain (module.js:501:10)
    at startup (node.js:129:16)
    at node.js:814:3
"""),
)


@pytest.mark.parametrize('test', tests)
def test_match(mocker, monkeypatch, test):
    mocker.patch('os.path.isfile', return_value=True)
    monkeypatch.setenv('EDITOR', 'dummy_editor')
    assert match(Command(stderr=test[4]), None)


@pytest.mark.parametrize('test', tests)
def test_no_editor(mocker, monkeypatch, test):
    mocker.patch('os.path.isfile', return_value=True)
    if 'EDITOR' in os.environ:
        monkeypatch.delenv('EDITOR')

    assert not match(Command(stderr=test[4]), None)


@pytest.mark.parametrize('test', tests)
def test_not_file(mocker, monkeypatch, test):
    mocker.patch('os.path.isfile', return_value=False)
    monkeypatch.setenv('EDITOR', 'dummy_editor')

    assert not match(Command(stderr=test[4]), None)


@pytest.mark.parametrize('test', tests)
def test_get_new_command(monkeypatch, test):
    monkeypatch.setenv('EDITOR', 'dummy_editor')
    assert (get_new_command(Command(script=test[0], stderr=test[4]), None) ==
        'dummy_editor {} +{} && {}'.format(test[1], test[2], test[0]))
